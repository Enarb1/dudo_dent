from datetime import datetime

from django.conf import settings
from googleapiclient.errors import HttpError

from Dudo_dent.appointments.utils import get_calendar_service
import logging
logger = logging.getLogger(__name__)

class GoogleCalendarService:
    """Class for Create, Update, and Delete Google Calendar events"""

    def __init__(self, appointment):
        self.service = get_calendar_service()
        self.appointment = appointment
        self.dentist = appointment.dentist
        self.profile = self.dentist.get_profile()

        if not self.profile or not self.profile.google_calendar_id:
            raise ValueError(f"{self.dentist.full_name} has no dedicated Google Calendar.")

    def _build_event_body(self):
        start_datetime = datetime.combine(self.appointment.date, self.appointment.start_time)
        end_datetime = datetime.combine(self.appointment.date, self.appointment.end_time)

        event = {
            'summary': f'{self.appointment.patient.full_name}',
            'description': f'{self.appointment.additional_info}' or '',
            'start': {
                'dateTime': start_datetime.isoformat(),
                'timeZone': 'Europe/Sofia',
            },
            'end': {
                'dateTime': end_datetime.isoformat(),
                'timeZone': 'Europe/Sofia',
            },
            'reminders': {
                'useDefault': True,
            }
        }

        return event

    def add(self):
        event = self._build_event_body()

        created_event = self.service.events().insert(
            calendarId=self.profile.google_calendar_id,
            body=event
        ).execute()

        self.appointment.google_event_id = created_event['id']
        self.appointment.save()

        return created_event

    def update(self):
        if not self.appointment.google_event_id:
            raise ValueError(f"No event in Google Calendar for this appointment.")

        event = self._build_event_body()

        updated_event = self.service.events().update(
        calendarId=self.profile.google_calendar_id,
        eventId=self.appointment.google_event_id,
        body=event
        ).execute()

        return updated_event

    def delete(self):
        if not self.appointment.google_event_id:
            raise ValueError(f"No event in Google Calendar for this appointment.")

        self.service.events().delete(
            calendarId=self.profile.google_calendar_id,
            eventId=self.appointment.google_event_id
        ).execute()


class GoogleCalendarManager:
    """
    A class used to create or delete Dentist Calendars in the main Google Calendar.
    In the create() method we set an ACL rule (Access Control List) to make sure
    that we can see the calendar in our Google Calendar Account.
    The Calendar name is a combination of the dentist name and his pk e.g. "dr.John Doe - id:1"
    """
    def __init__(self):
        self.service = get_calendar_service()

    def create(self, dentist_name, pk):
        calendar = {
            'summary': f'dr.{dentist_name} - id:{pk}',
            'timeZone': 'Europe/Sofia',
        }

        created_calendar = self.service.calendars().insert(
            body=calendar,
        ).execute()

        acl_rule = {
            'scope': {
                'type': 'user',
                'value': settings.GOOGLE_ADMIN_EMAIL
            },
            'role': 'owner'
        }

        try:
            self.service.acl().insert(calendarId=created_calendar['id'], body=acl_rule).execute()
            print(f'Calendar shared with {settings.GOOGLE_ADMIN_EMAIL} successfully.')
        except HttpError as error:
            print(f'Failed to share calendar with {settings.GOOGLE_ADMIN_EMAIL}: {error.status_code} - {error}.')

        return created_calendar['id']

    def delete(self, calendar_id):
        try:
            self.service.calendars().delete(calendarId=calendar_id).execute()
            print(f'Calendar deleted successfully.')
            return True
        except HttpError as he:
            print(f"Error deleting calendar {calendar_id}: {he}")
            return False
