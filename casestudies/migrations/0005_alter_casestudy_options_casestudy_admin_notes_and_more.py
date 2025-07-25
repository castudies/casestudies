# Generated by Django 4.2.14 on 2025-06-27 04:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casestudies', '0004_alter_casestudy_expert_solution'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='casestudy',
            options={'ordering': ['-created_at'], 'verbose_name': 'Case Study', 'verbose_name_plural': 'Case Studies'},
        ),
        migrations.AddField(
            model_name='casestudy',
            name='admin_notes',
            field=models.TextField(blank=True, help_text='Admin notes for approval/rejection'),
        ),
        migrations.AddField(
            model_name='casestudy',
            name='is_approved',
            field=models.BooleanField(default=False, help_text='Whether this case study has been approved for publication'),
        ),
        migrations.AddField(
            model_name='casestudy',
            name='submitted_at',
            field=models.DateTimeField(default=datetime.datetime.now, help_text='When this case study was submitted'),
        ),
        migrations.AddField(
            model_name='casestudy',
            name='submitter_email',
            field=models.EmailField(blank=True, help_text='Email address of the person who submitted this case study', max_length=254, null=True),
        ),
    ]
