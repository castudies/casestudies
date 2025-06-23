from django.db import models
from typing import TYPE_CHECKING, ClassVar
from django.utils.text import slugify
import os

# Create your models here.
if TYPE_CHECKING:
    from django.db.models.manager import Manager


class CaseStudy(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100, blank=True, default='')
    author_url = models.URLField(max_length=200, blank=True, null=True, help_text="URL for the author's profile or website.")
    thumbnail = models.ImageField(upload_to='thumbnails/', help_text="For best results, use an image that is 1584px wide by 396px tall and content centered.")
    
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='Easy')
    domain = models.CharField(max_length=100, blank=True)
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags (e.g., SQL, Python, EDA, Business)")
    
    case_background = models.TextField(blank=True)
    data_summary = models.TextField(blank=True)
    dataset = models.FileField(upload_to='datasets/', blank=True, null=True, help_text="Upload the dataset file (CSV, Excel, etc.)")
    task = models.TextField(blank=True)
    expert_solution = models.TextField(blank=True)

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
