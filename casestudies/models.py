from django.db import models
from typing import TYPE_CHECKING, ClassVar
from django.utils.text import slugify
import os
from datetime import datetime
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field

if TYPE_CHECKING:
    from django.db.models.manager import Manager


def upload_with_timestamp(instance, filename):
    base, ext = os.path.splitext(filename)
    now = datetime.now()
    timestamp = now.strftime('%H%M%d%m%y')
    new_filename = f"{base}_{timestamp}{ext}"
    if 'thumbnail' in instance._meta.get_field('thumbnail').attname:
        return os.path.join('thumbnails', new_filename)
    else:
        return os.path.join('datasets', new_filename)


class CaseStudy(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    DOMAIN_CHOICES = [
        ("Business & Marketing", "Business & Marketing"),
        ("Sales & Revenue", "Sales & Revenue"),
        ("Finance", "Finance"),
        ("Healthcare & Medical", "Healthcare & Medical"),
        ("Retail & E-commerce", "Retail & E-commerce"),
        ("Web & App", "Web & App"),
        ("Social Media & Influencer", "Social Media & Influencer"),
        ("Supply Chain & Logistics", "Supply Chain & Logistics"),
        ("Education", "Education"),
        ("Government & Public Sector", "Government & Public Sector"),
        ("Manufacturing & Operations", "Manufacturing & Operations"),
        ("Energy & Environment", "Energy & Environment"),
        ("Real Estate & Property", "Real Estate & Property"),
        ("Sports & Fitness", "Sports & Fitness"),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100, blank=True, default='')
    author_url = models.URLField(max_length=200, blank=True, null=True, help_text="URL for the author's profile or website.")
    thumbnail = models.ImageField(upload_to=upload_with_timestamp, help_text="For best results, use an image that is 1584px wide by 396px tall and content centered.")

    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='Easy')
    domain = models.CharField(max_length=100, blank=True, choices=DOMAIN_CHOICES)
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags (e.g., SQL, Python, EDA, Business)")

    case_background = models.TextField(blank=True)
    data_summary = models.TextField(blank=True)
    dataset = models.FileField(upload_to=upload_with_timestamp, blank=True, null=True, help_text="Upload the dataset file (CSV, Excel, etc.)")
    task = models.TextField(blank=True)
    expert_solution = CKEditor5Field(blank=True, config_name='extends')

    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    if TYPE_CHECKING:
        objects: ClassVar[Manager]

    @property
    def dataset_filename(self):
        if self.dataset:
            return os.path.basename(str(self.dataset.name))
        return ''

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('casestudies:case_study_detail', kwargs={'slug': self.slug})


class Notification(models.Model):
    title = models.CharField(max_length=200, help_text="Main heading for the notification pop-up.")
    body = models.TextField(help_text="Body text for the notification pop-up.")
    video = models.FileField(upload_to='notifications/', blank=True, null=True, help_text="Optional video for the notification pop-up.")
    button_text = models.CharField(max_length=100, default="Share", help_text="Text for the notification button.")
    button_link = models.URLField(max_length=300, blank=True, help_text="URL the button should link to.")
    is_active = models.BooleanField(default=True, help_text="Show this notification on the homepage?")
    delay_seconds = models.PositiveIntegerField(default=10, help_text="How many seconds after page load the notification should appear.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
