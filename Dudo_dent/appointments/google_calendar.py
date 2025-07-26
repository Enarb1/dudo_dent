from datetime import datetime

from django.conf import settings
from googleapiclient.errors import HttpError

from Dudo_dent.appointments.utils import get_calendar_service


class GoogleCalendarService:

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


def create_calendar(name, pk):
    """
        This creates a calendar within the Google Calendar.
        We set the calendar name and the timezone.
        in the 'acl_rule' we set the access control list(ACL)
        with which we make sure that the main account sees the
        newly created calendar (which is created to the service account).
    """
    service = get_calendar_service()

    calendar = {
        'summary': f"{name}({pk})",
        'timezone': 'Europe/Sofia'
    }

    created_calendar =service.calendars().insert(body=calendar).execute()


    acl_rule = {
        'scope': {
            'type': 'user',
            'value': settings.GOOGLE_ADMIN_EMAIL
        },
        'role': 'owner'
    }

    try:
        service.acl().insert(calendarId=created_calendar['id'], body=acl_rule).execute()
        print(f'Calendar shared with {settings.GOOGLE_ADMIN_EMAIL} successfully.')
    except HttpError as error:
        print(f'Failed to share calendar with {settings.GOOGLE_ADMIN_EMAIL}: {error.status_code} - {error}.')


    return created_calendar['id']







# def get_calendar_service():
#     """Builds and returns a Google Calendar service client using service account credentials."""
#     credentials = service_account.Credentials.from_service_account_file(
#         settings.GOOGLE_SERVICE_ACCOUNT_FILE,
#         scopes=SCOPES,
#     )
#
#     service = build('calendar', 'v3', credentials=credentials)
#
#     return service





# def get_event_info(appointment):
#     start_datetime = datetime.combine(appointment.date, appointment.start_time)
#     end_datetime = datetime.combine(appointment.date, appointment.end_time)
#
#     event = {
#         'summary': f'{appointment.patient.full_name}',
#         'description': f'{appointment.additional_info}' or '',
#         'start': {
#             'dateTime': start_datetime.isoformat(),
#             'timeZone': 'Europe/Sofia',
#         },
#         'end': {
#             'dateTime': end_datetime.isoformat(),
#             'timeZone': 'Europe/Sofia',
#         },
#         'reminders': {
#             'useDefault': True,
#         }
#     }
#
#     return event



# def add_appointment_to_google_calendar(appointment):
#     """
#     Adding the appointment in the dedicated Google Calendar for the Dentist.
#     """
#     service = get_calendar_service()
#     dentist = appointment.dentist
#     profile = dentist.get_profile()
#
#     if not profile or not profile.google_calendar_id:
#         raise ValueError(f"{dentist.full_name} has no dedicated Google Calendar.")
#
#     event = get_event_info(appointment)
#
#     created_event = service.events().insert(
#         calendarId=profile.google_calendar_id,
#         body=event
#     ).execute()
#
#     appointment.google_event_id = created_event['id']
#     appointment.save()
#
#     return created_event
#
#
#
# def edit_appointment_in_google_calendar(appointment):
#     service = get_calendar_service()
#     dentist  = appointment.dentist
#     profile = dentist.get_profile()
#
#     if not profile or not profile.google_calendar_id:
#         raise ValueError(f"{dentist.full_name} has no dedicated Google Calendar.")
#
#     if not appointment.google_event_id:
#         raise ValueError(f"No event in Google Calendar for this appointment.")
#
#
#     event = get_event_info(appointment)
#
#     updated_event = service.events().update(
#         calendarId=profile.google_calendar_id,
#         eventId=appointment.google_event_id,
#         body=event
#     ).execute()
#
#     return updated_event
#
#
# #TODO
# def delete_appointment_from_google_calendar():
#     pass















