from django import forms
from .models import UserSubmittedCaseStudy
from django.core.files.uploadedfile import UploadedFile
import os
import re
from PIL import Image
import magic  # You may need to install python-magic for MIME type checking
from django.core.files.base import ContentFile

ALLOWED_DATASET_EXTENSIONS = ['.csv', '.xlsx', '.xls', '.txt']
ALLOWED_DATASET_MIME_TYPES = [
    'text/csv',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-excel',
    'text/plain',
]

# Helper to sanitize filenames
def sanitize_filename(filename):
    filename = os.path.basename(filename)
    filename = re.sub(r'[^\w\-.]', '_', filename)
    return filename

class CaseStudySubmissionForm(forms.ModelForm):
    class Meta:
        model = UserSubmittedCaseStudy
        fields = [
            'title', 'author', 'submitter_email', 'domain', 'difficulty', 
            'tags', 'case_background', 'task', 'expert_solution', 'options', 'dataset', 'thumbnail'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter the case study title'
            }),
            'author': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Your name'
            }),
            'submitter_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'your.email@example.com'
            }),
            'domain': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'difficulty': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'e.g., SQL, Python, EDA, Business (comma-separated)'
            }),
            'case_background': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Describe the background and context of the case study.'
            }),
            'task': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Describe the specific task or problem to be solved.'
            }),
            'thumbnail': forms.ClearableFileInput(attrs={
                'class': 'image-upload-input',
                'accept': 'image/png,image/jpeg,image/jp2',
            }),
        }

    def clean_dataset(self):
        dataset = self.cleaned_data.get('dataset')
        if dataset:
            # Check file size
            if dataset.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Dataset file size must not exceed 5 MB.')
            # Check extension
            ext = os.path.splitext(dataset.name)[1].lower()
            if ext not in ALLOWED_DATASET_EXTENSIONS:
                raise forms.ValidationError('Only CSV, Excel, and TXT files are allowed.')
            # Check MIME type using magic
            try:
                mime = magic.from_buffer(dataset.read(2048), mime=True)
                dataset.seek(0)
            except Exception:
                raise forms.ValidationError('Could not determine file type. Please upload a valid file.')
            if mime not in ALLOWED_DATASET_MIME_TYPES:
                raise forms.ValidationError('Invalid file type. Only CSV, Excel, and TXT files are allowed.')
            # Sanitize filename
            dataset.name = sanitize_filename(dataset.name)
        return dataset

    def clean_thumbnail(self):
        thumbnail = self.cleaned_data.get('thumbnail')
        if thumbnail:
            # Check file size
            if hasattr(thumbnail, 'size') and thumbnail.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Thumbnail image size must not exceed 2 MB.')
            # Check MIME type
            if isinstance(thumbnail, UploadedFile):
                if not thumbnail.content_type in ['image/jpeg', 'image/png', 'image/jp2']:
                    raise forms.ValidationError('Only JPG, JPEG2000, and PNG images are allowed.')
            # Validate image content using Pillow
            try:
                image = Image.open(thumbnail)
                image.verify()  # Will raise if not a valid image
                thumbnail.seek(0)
            except Exception:
                raise forms.ValidationError('Uploaded file is not a valid image.')
            # Sanitize filename
            thumbnail.name = sanitize_filename(thumbnail.name)
        return thumbnail

# Admin ModelForm to ensure 'slug' is included
class UserSubmittedCaseStudyAdminForm(forms.ModelForm):
    class Meta:
        model = UserSubmittedCaseStudy
        fields = '__all__'

    def clean_dataset(self):
        dataset = self.cleaned_data.get('dataset')
        if dataset and dataset.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Dataset file size must not exceed 5 MB.')
        return dataset

    def clean_thumbnail(self):
        thumbnail = self.cleaned_data.get('thumbnail')
        if thumbnail:
            if hasattr(thumbnail, 'size') and thumbnail.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Thumbnail image size must not exceed 2 MB.')
            if isinstance(thumbnail, UploadedFile):
                if not thumbnail.content_type in ['image/jpeg', 'image/png', 'image/jp2']:
                    raise forms.ValidationError('Only JPG, JPEG2000, and PNG images are allowed.')
        return thumbnail 