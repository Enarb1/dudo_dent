from django.apps import AppConfig


class AppointmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Dudo_dent.appointments'


    def ready(self):
        import Dudo_dent.appointments.signals