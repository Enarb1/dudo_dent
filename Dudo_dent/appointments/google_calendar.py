from datetime import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """Builds and returns a Google Calendar service client using service account credentials."""
    credentials = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_SERVICE_ACCOUNT_FILE,
        scopes=SCOPES,
    )

    service = build('calendar', 'v3', credentials=credentials)

    return service


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


def add_appointment_to_google_calendar(appointment, dentist, patient):
    """
    Adding the appointment in the dedicated Google Calendar for the Dentist.
    """
    service = get_calendar_service()

    profile = dentist.get_profile()

    if not profile or not profile.google_calendar_id:
        raise ValueError(f"{dentist.full_name} has no dedicated Google Calendar.")

    start_datetime = datetime.combine(appointment.date, appointment.start_time)
    end_datetime = datetime.combine(appointment.date, appointment.end_time)

    event = {
        'summary': f'{patient.full_name}',
        'description': f'{appointment.additional_info}' or '',
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

    created_event = service.events().insert(
        calendarId=profile.google_calendar_id,
        body=event
    ).execute()
    print(created_event)

    appointment.google_event_id = created_event['id']
    appointment.save()


    return created_event



#TODO
def edit_appointment_in_google_calendar():
    pass


#TODO
def delete_appointment_from_google_calendar():
    pass















