from django.contrib.auth.models import Group

from Dudo_dent.accounts.models import WorkProfile
from Dudo_dent.patients.models import Patient


ROLE_GROUP_MAP = {
    'nurse': 'Nurse',
    'dentist': 'Dentist',
}

def handle_patient_profile(user):
    try:
        personal_id = getattr(user, 'personal_id', None)
        patient = Patient.objects.get(personal_id=personal_id)
        patient.user = user
        patient.email = user.email
        patient.save()
    except Patient.DoesNotExist:
        Patient.objects.create(
            user=user,
            full_name=user.full_name,
            email=user.email,
            age=getattr(user, 'age', None),
            phone_number=getattr(user, 'phone_number', None),
            personal_id=getattr(user, 'personal_id', None),
            gender=getattr(user, 'gender', None),
        )


def handle_work_profile(user):
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



