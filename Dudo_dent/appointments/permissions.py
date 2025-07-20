def has_calender_access(user):
    return user.is_authenticated and (
        user.is_dentist or
        user.is_nurse or
        user.is_staff
    )