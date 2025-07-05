def get_profile_fields(field_map, profile, user):
    profile_fields = []

    for field_name, field_label in field_map.items():

        """In value we check the value of the field. We check both user and profile, 
        as the field name can come either form CustomUser, WorkProfile or PatientRegister"""
        value = getattr(profile, field_name, None) or getattr(user, field_name, None)

        if value:
            profile_fields.append((field_label, value))

    return profile_fields