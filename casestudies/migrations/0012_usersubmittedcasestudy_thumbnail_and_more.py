# Generated by Django 4.2.14 on 2025-06-27 07:59

import casestudies.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casestudies', '0011_alter_usersubmittedcasestudy_domain'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersubmittedcasestudy',
            name='thumbnail',
            field=models.ImageField(blank=True, help_text='Upload a thumbnail image (JPG, JPEG2000, PNG, ≤2MB). For best results, use an image that is 1584px wide by 396px tall and content centered.', null=True, upload_to=casestudies.models.UserSubmittedCaseStudy.user_thumbnail_upload_path),
        ),
        migrations.AlterField(
            model_name='usersubmittedcasestudy',
            name='dataset',
            field=models.FileField(blank=True, help_text='Upload a dataset file (CSV, Excel, etc.)', null=True, upload_to=casestudies.models.user_upload_with_timestamp),
        ),
    ]
