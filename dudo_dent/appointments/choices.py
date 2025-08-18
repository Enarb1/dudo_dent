from django.db import models


class WeekdayChoices(models.TextChoices):
    MONDAY = "1", "Понеденик"
    TUESDAY = "2", "Вторник"
    WEDNESDAY = "3", "Сряда"
    THURSDAY = "4", "Четвъртък"
    FRIDAY = "5", "Петък"
    SATURDAY = "6", "Събота"
    SUNDAY = "7", "Неделя"