from django.contrib.auth.models import Group

from Dudo_dent.accounts.models import WorkProfile
from Dudo_dent.patients.models import Patient
import logging
logger = logging.getLogger(__name__)

ROLE_GROUP_MAP = {
    'nurse': 'Nurse',
    'dentist': 'Dentist',
}

def handle_patient_profile(user):
    """
    This function checks if the patient user has already a patient profile.
    It connects the profiles by personal ID.
    If there is no patient profile in the Patient DB , it creates a one.
    """

    try:
        patient = Patient.objects.get(email=user.email)
        patient.user = user
        patient.full_name = user.full_name if user.full_name else patient.full_name
        patient.date_of_birth = getattr(user, 'date_of_birth', patient.date_of_birth)
        patient.personal_id = getattr(user, 'personal_id', patient.personal_id)
        patient.phone_number = getattr(user, 'phone_number', patient.phone_number)
        patient.gender = getattr(user, 'gender', patient.gender)
        patient.save()
    except Patient.DoesNotExist:
        Patient.objects.create(
            user=user,
            full_name=user.full_name,
            email=user.email,
            date_of_birth=getattr(user, 'date_of_birth', None),
            phone_number=getattr(user, 'phone_number', None),
            personal_id=getattr(user, 'personal_id', None),
            gender=getattr(user, 'gender', None),
        )


def handle_work_profile(user):
    """
    Creating a WorkProfile object for the user - dentist or nurse.
    Also assigning the appropriate permissions to the WorkProfile.
    """
    WorkProfile.objects.create(
        user=user,
        phone_number=getattr(user, 'phone_number', None),
        address=getattr(user, 'address', None),
        date_of_birth=getattr(user, 'date_of_birth', None),
    )

    permission_group = ROLE_GROUP_MAP.get(user.role.lower(), None)

    if permission_group:
        try:
            group = Group.objects.get(name=permission_group)
            user.groups.add(group)
        except Group.DoesNotExist:
            print(f"Group '{permission_group}' does not exist.")



