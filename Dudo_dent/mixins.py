from Dudo_dent.accounts.models import CustomUser


class GetDentistsMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dentists = [d for d in CustomUser.objects.all() if d.is_dentist]
        self.fields['dentist'].choices = [(d.id, d.username) for d in dentists]

