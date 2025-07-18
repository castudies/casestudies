# Generated by Django 4.2.14 on 2025-06-26 06:21

import casestudies.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CaseStudy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(blank=True, default='', max_length=100)),
                ('author_url', models.URLField(blank=True, help_text="URL for the author's profile or website.", null=True)),
                ('thumbnail', models.ImageField(help_text='For best results, use an image that is 1584px wide by 396px tall and content centered.', upload_to=casestudies.models.upload_with_timestamp)),
                ('difficulty', models.CharField(choices=[('Easy', 'Easy'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], default='Easy', max_length=20)),
                ('domain', models.CharField(blank=True, choices=[('Business & Marketing', 'Business & Marketing'), ('Sales & Revenue', 'Sales & Revenue'), ('Finance', 'Finance'), ('Healthcare & Medical', 'Healthcare & Medical'), ('Retail & E-commerce', 'Retail & E-commerce'), ('Web & App', 'Web & App'), ('Social Media & Influencer', 'Social Media & Influencer'), ('Supply Chain & Logistics', 'Supply Chain & Logistics'), ('Education', 'Education'), ('Government & Public Sector', 'Government & Public Sector'), ('Manufacturing & Operations', 'Manufacturing & Operations'), ('Energy & Environment', 'Energy & Environment'), ('Real Estate & Property', 'Real Estate & Property'), ('Sports & Fitness', 'Sports & Fitness')], max_length=100)),
                ('tags', models.CharField(blank=True, help_text='Comma-separated tags (e.g., SQL, Python, EDA, Business)', max_length=500)),
                ('case_background', models.TextField(blank=True)),
                ('data_summary', models.TextField(blank=True)),
                ('dataset', models.FileField(blank=True, help_text='Upload the dataset file (CSV, Excel, etc.)', null=True, upload_to=casestudies.models.upload_with_timestamp)),
                ('task', models.TextField(blank=True)),
                ('expert_solution', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
        ),
    ]
