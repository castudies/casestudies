from django import forms
from .models import UserSubmittedCaseStudy
from django.core.files.uploadedfile import UploadedFile
import os
import re
from PIL import Image
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

# Helper function to check file type using extension and content type
def validate_file_type(file, allowed_extensions, allowed_mime_types):
    """
    Validate file type using both extension and content type.
    Returns True if valid, raises ValidationError if invalid.
    """
    # Check extension
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in allowed_extensions:
        raise forms.ValidationError(f'Invalid file extension. Allowed extensions: {", ".join(allowed_extensions)}')
    
    # Check content type if available
    if hasattr(file, 'content_type') and file.content_type:
        if file.content_type not in allowed_mime_types:
            raise forms.ValidationError(f'Invalid file type. Allowed types: {", ".join(allowed_mime_types)}')
    
    return True

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
            
            # Validate file type using extension and content type
            try:
                validate_file_type(dataset, ALLOWED_DATASET_EXTENSIONS, ALLOWED_DATASET_MIME_TYPES)
            except forms.ValidationError as e:
                raise e
            
            # Additional validation for specific file types
            ext = os.path.splitext(dataset.name)[1].lower()
            if ext == '.csv':
                # For CSV files, we can do additional validation if needed
                try:
                    # Read first few bytes to check if it looks like CSV
                    dataset.seek(0)
                    first_bytes = dataset.read(1024).decode('utf-8', errors='ignore')
                    dataset.seek(0)
                    # Basic CSV validation - check if it contains commas or semicolons
                    if not (',' in first_bytes or ';' in first_bytes):
                        raise forms.ValidationError('File does not appear to be a valid CSV file.')
                except UnicodeDecodeError:
                    raise forms.ValidationError('File encoding is not supported. Please use UTF-8 encoding.')
            
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
            # Validate image content and dimensions using Pillow
            try:
                image = Image.open(thumbnail)
                image.verify()  # Will raise if not a valid image
                thumbnail.seek(0)  # Reset file pointer after verify
                
                # Check image dimensions
                image = Image.open(thumbnail)  # Open again for dimension checking
                width, height = image.size
                
                # Set reasonable limits for thumbnail images
                MAX_WIDTH = 2048
                MAX_HEIGHT = 2048
                MIN_WIDTH = 50
                MIN_HEIGHT = 50
                
                if width > MAX_WIDTH or height > MAX_HEIGHT:
                    raise forms.ValidationError(f'Image dimensions must not exceed {MAX_WIDTH}x{MAX_HEIGHT} pixels. Current size: {width}x{height}')
                
                if width < MIN_WIDTH or height < MIN_HEIGHT:
                    raise forms.ValidationError(f'Image dimensions must be at least {MIN_WIDTH}x{MIN_HEIGHT} pixels. Current size: {width}x{height}')
                
                thumbnail.seek(0)  # Reset file pointer
            except Exception as e:
                if isinstance(e, forms.ValidationError):
                    raise e
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