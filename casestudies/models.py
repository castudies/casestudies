from django.db import models
from django.utils.text import slugify

# Create your models here.

class CaseStudy(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='thumbnails/', help_text="For best results, use an image that is 370px wide by 160px tall.")
    
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='Easy')
    domain = models.CharField(max_length=100, blank=True)
    
    case_background = models.TextField(blank=True)
    data_summary = models.TextField(blank=True)
    task = models.TextField(blank=True)
    expert_solution = models.TextField(blank=True)
    loves = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    summary_image1 = models.ImageField(upload_to='summary_images/', blank=True, null=True, help_text="Recommended size: 384x256px (3:2 or 4:3 aspect ratio). Larger images will be scaled down.")
    summary_image2 = models.ImageField(upload_to='summary_images/', blank=True, null=True, help_text="Recommended size: 384x256px (3:2 or 4:3 aspect ratio). Larger images will be scaled down.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
