def get_profile_fields(field_map, profile, user):
    profile_fields = []

    for field_name, field_label in field_map.items():

        """In value we check the value of the field. 
        First we check in the profile and if it is None, we check in user"""
        value = getattr(profile, field_name, None)

        if value is None and user is not None:
            value = getattr(user, field_name, None)

        display_value = value if value not in (None, "") else "N/A"
        profile_fields.append((field_label, display_value))

    return profile_fields