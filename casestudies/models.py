from django.db import models
from django.utils.text import slugify
import os

# Create your models here.

class CaseStudy(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100, blank=True, default='')
    thumbnail = models.ImageField(upload_to='thumbnails/', help_text="For best results, use an image that is 370px wide by 160px tall.")
    
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='Easy')
    domain = models.CharField(max_length=100, blank=True)
    
    case_background = models.TextField(blank=True)
    data_summary = models.TextField(blank=True)
    dataset = models.FileField(upload_to='datasets/', blank=True, null=True, help_text="Upload the dataset file (CSV, Excel, etc.)")
    task = models.TextField(blank=True)
    expert_solution = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    @property
    def dataset_filename(self):
        if self.dataset:
            return os.path.basename(self.dataset.name)
        return ''

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
