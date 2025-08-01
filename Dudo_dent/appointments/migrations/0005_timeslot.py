# Generated by Django 5.2 on 2025-07-22 16:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0004_appointment_additional_info'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('is_available', models.BooleanField(default=True)),
                ('google_event_id', models.CharField(blank=True, max_length=255, null=True)),
                ('dentist', models.ForeignKey(limit_choices_to={'role': 'dentist'}, on_delete=django.db.models.deletion.CASCADE, related_name='time_slots', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
