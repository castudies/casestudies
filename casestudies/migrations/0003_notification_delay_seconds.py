# Generated by Django 4.2.14 on 2025-06-26 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casestudies', '0002_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='delay_seconds',
            field=models.PositiveIntegerField(default=10, help_text='How many seconds after page load the notification should appear.'),
        ),
    ]
