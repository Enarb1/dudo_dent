from datetime import date, timedelta, datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings

from Dudo_dent.appointments.models import Appointment, AvailabilityRule, UnavailabilityRule

import logging
logger = logging.getLogger(__name__)

def get_calendar_service():
    """
    Getting the Google Calendar service.
    """
    credentials = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/calendar'],
    )
    service = build('calendar', 'v3', credentials=credentials)

    return service


def get_appointments_for_today(user):
    """
    This returns all appointments for the day for the dentist and
    All future appointments for the patient.
    We show this info in the home view of both patient and dentist
    """
    today = date.today()

    if not user.is_authenticated:
        return Appointment.objects.none()

    if user.is_patient:
        return Appointment.objects.filter(patient__user_id=user.id, date__gte=today).order_by('date')
    if user.is_dentist:
        return Appointment.objects.filter(dentist_id=user.id, date=today).order_by('date')

    return Appointment.objects.filter(date=today)


def clear_booking_session(session):
    """
    With this helper function we clean the additional session keys,
    which were added during the booking session
    """

    keys = [
        'appointment_step1_data',
        'appointment_step2_data',
        'appointment_step3_data',
        'patient_id',
        'dentist_id',
        'date',
    ]
    for key in keys:
        session.pop(key, None)

def get_dentist_available_dates(dentist_id):
    """
    Getting all the available dates according to the availability set for a dentist.
    """

    today = date.today()

    availability_rules= AvailabilityRule.objects.filter(
        dentist_id=dentist_id,
        valid_to__gte=today,
    )

    unavailability_rules = UnavailabilityRule.objects.filter(
        dentist_id=dentist_id,
        end_date__gte=today,
    )

    unavailable_dates = set()

    for rule in unavailability_rules:
        current = rule.start_date
        while current <= rule.end_date:
            unavailable_dates.add(current)
            current += timedelta(days=1)

    available_dates = set()

    for rule in availability_rules:
        start_date = max(today, rule.valid_from)
        end_date = rule.valid_to
        current = start_date

        while current <= end_date:
            weekday_str = str(current.isoweekday())
            if weekday_str in rule.weekdays and current not in unavailable_dates:
                available_dates.add(current)
            current += timedelta(days=1)

    return sorted(available_dates)

def get_available_time_slots(dentist_id, selected_date):
    """
     We get all the available timeslots for a dentist for a specific date.
     First we get all rules applying to the selected date.
     Then we get the weekday for the selected date, which we use to check if the rule
     applies to the selected weekday. If so, we get all timeslots (15min) for that date.
     After this we create a list with all bookings for the selected date
     and we generate all available timeslots, which are not booked.
    """

    if UnavailabilityRule.objects.filter(
            dentist_id=dentist_id,
            start_date__lte=selected_date,
            end_date__gte=selected_date,
    ).exists():
        return []

    rules = AvailabilityRule.objects.filter(
        dentist_id=dentist_id,
        valid_from__lte=selected_date,
        valid_to__gte=selected_date,
    )

    weekday_str = str(selected_date.isoweekday())
    time_slots = []

    for rule in rules:
        if weekday_str not in rule.weekdays:
            continue

        start_time = datetime.combine(selected_date, rule.start_time)
        end_time = datetime.combine(selected_date, rule.end_time)
        current = start_time

        while current + timedelta(minutes=15) <= end_time:
            time_slots.append(current.time())
            current += timedelta(minutes=15)

    booked_times = Appointment.objects.filter(
        dentist_id=dentist_id,
        date=selected_date,
    ).values_list('start_time', flat=True)

    available_time_slots = [slot for slot in time_slots if slot not in booked_times]

    return available_time_slots

