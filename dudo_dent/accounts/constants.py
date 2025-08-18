from dudo_dent.accounts.choices import UserTypeChoices
from dudo_dent.accounts.services.user_profile_services import handle_patient_profile, handle_work_profile

ALLOWED_ROLES_CREATION = {
    UserTypeChoices.ADMIN: [
        UserTypeChoices.PATIENT, UserTypeChoices.ADMIN, UserTypeChoices.NURSE, UserTypeChoices.DENTIST
    ],
    UserTypeChoices.NURSE: [UserTypeChoices.NURSE],
    UserTypeChoices.DENTIST: [UserTypeChoices.DENTIST, UserTypeChoices.NURSE]
}

USER_IS_STAFF = {
    UserTypeChoices.ADMIN: True,
    UserTypeChoices.NURSE: False,
    UserTypeChoices.DENTIST: False,
    UserTypeChoices.PATIENT: False,
}

ROLE_PROFILE_HANDLERS = {
    UserTypeChoices.PATIENT: handle_patient_profile,
    UserTypeChoices.NURSE: handle_work_profile,
    UserTypeChoices.DENTIST: handle_work_profile,
}

PATIENT_PROFILE_FIELDS = {
    'full_name': 'Име',
    'email': 'Email',
    'phone_number': 'Телефон',
    'personal_id': 'ЕГН',
    'gender': 'Пол',
    'age': 'Години',
}

WORK_PROFILE_FIELDS = {
    'full_name': 'Име',
    'email': 'Email',
    'phone_number': 'Телефон',
    'address': 'Адрес',
    'age': 'Години',
}

APPOINTMENT_FIELDS = {
    'patient': 'Име',
    'dentist': 'Д-р',
    'datetime_display': 'Дата',
    'additional_info': 'Допълнителна информация',
}



