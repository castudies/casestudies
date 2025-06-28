from django.db import models
from typing import TYPE_CHECKING, ClassVar
from django.utils.text import slugify
import os
from datetime import datetime
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from django.utils import timezone

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


def user_upload_with_timestamp(instance, filename):
    base, ext = os.path.splitext(filename)
    now = datetime.now()
    timestamp = now.strftime('%H%M%d%m%y')
    new_filename = f"{base}_{timestamp}{ext}"
    return os.path.join('user_datasets', new_filename)


class CaseStudy(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
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

    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
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

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Case Study"
        verbose_name_plural = "Case Studies"


class Notification(models.Model):
    title = models.CharField(max_length=200, help_text="Main heading for the notification pop-up.")
    body = models.TextField(help_text="Body text for the notification pop-up.")
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


class UserSubmittedCaseStudy(models.Model):
    """Model for user-submitted case studies that need admin approval"""
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
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
    
    # Basic Information
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    author = models.CharField(max_length=100)
    submitter_email = models.EmailField(help_text="Email of the person submitting the case study")
    domain = models.CharField(max_length=100, choices=DOMAIN_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    tags = models.TextField(blank=True, help_text="Comma-separated tags")
    
    # Content
    case_background = models.TextField()
    task = models.TextField()
    expert_solution = CKEditor5Field(config_name='extends')
    options = models.TextField(blank=True)
    dataset = models.FileField(upload_to=user_upload_with_timestamp, blank=True, null=True, help_text='Upload a dataset file (CSV, Excel, etc.)')
    
    # Approval Status
    is_approved = models.BooleanField(null=True, blank=True, help_text="True=Approved, False=Rejected, Null=Pending")
    admin_notes = models.TextField(blank=True, help_text="Notes from admin about approval/rejection")
    
    # Timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Thumbnail
    def user_thumbnail_upload_path(instance, filename):
        base, ext = os.path.splitext(filename)
        now = datetime.now()
        timestamp = now.strftime('%H%M%d%m%y')
        new_filename = f"{base}_{timestamp}{ext}"
        return os.path.join('user_thumbnails', new_filename)

    thumbnail = models.ImageField(
        upload_to=user_thumbnail_upload_path,
        blank=True,
        null=True,
        help_text="Upload a thumbnail image (JPG, JPEG2000, PNG, ≤2MB). For best results, use an image that is 1584px wide by 396px tall and content centered."
    )
    
    class Meta:
        verbose_name = "User Submitted Case Study"
        verbose_name_plural = "User Submitted Case Studies"
        ordering = ['-submitted_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        status = "Pending"
        if self.is_approved is True:
            status = "Approved"
        elif self.is_approved is False:
            status = "Rejected"
        return f"{self.title} by {self.author} ({status})"
    
    @property
    def status_display(self):
        if self.is_approved is None:
            return "Pending"
        elif self.is_approved:
            return "Approved"
        else:
            return "Rejected"

    @property
    def dataset_filename(self):
        if self.dataset:
            return os.path.basename(str(self.dataset.name))
        return ''

    def get_absolute_url(self):
        return reverse('casestudies:case_study_detail', kwargs={'slug': self.slug})


class UploadLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()
    email = models.EmailField()
    dataset = models.CharField(max_length=255, blank=True, null=True)
    thumbnail = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.timestamp} - {self.email} - {self.ip}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Upload Log"
        verbose_name_plural = "Upload Logs"
