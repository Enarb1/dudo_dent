from datetime import date


class AgeCalculatorMixin:
    @property
    def age(self):
        birth_date = getattr(self, 'date_of_birth', None)

        if not birth_date:
            return None
        today = date.today()
        """Using the True and False values in order to get 1 or 0. 
        If the birthday has passed we subtract with 1 else with 0."""
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))