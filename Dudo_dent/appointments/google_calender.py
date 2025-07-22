from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calender_service():
    """Builds and returns a Google Calendar service client using service account credentials."""
    credentials = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_SERVICE_ACCOUNT_FILE,
        scopes=SCOPES,
    )

    service = build('calendar', 'v3', credentials=credentials)

    return service


def create_calendar(name, pk):
    """access control list(ACL)"""
    service = get_calender_service()

    calendar = {
        'summary': f"{name}({pk})",
        'timezone': 'Europe/Sofia'
    }

    created_calender =service.calendars().insert(body=calendar).execute()


    acl_rule = {
        'scope': {
            'type': 'user',
            'value': settings.GOOGLE_ADMIN_EMAIL
        },
        'role': 'owner'
    }

    try:
        service.acl().insert(calendarId=created_calender['id'], body=acl_rule).execute()
        print(f'Calendar shared with {settings.GOOGLE_ADMIN_EMAIL} successfully.')
    except HttpError as error:
        print(f'Failed to share calendar with {settings.GOOGLE_ADMIN_EMAIL}: {error.status_code} - {error}.')


    return created_calender['id']