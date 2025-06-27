import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'unsafe-default-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['castudies.com', 'www.castudies.com']
CSRF_TRUSTED_ORIGINS = ['https://castudies.com', 'https://www.castudies.com']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'casestudies',
    'django.contrib.sitemaps',
    'storages',
    'django_ckeditor_5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'casestudy_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'casestudy_project.wsgi.application'

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'assets']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (uploaded user content to S3)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

# Additional S3 settings to fix upload issues
AWS_S3_VERIFY = True
AWS_S3_ADDRESSING_STYLE = 'virtual'
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_QUERYSTRING_AUTH = False
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_S3_CUSTOM_DOMAIN = 'cdn.castudies.com'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {'format': '[{asctime}] {levelname} {name} {message}', 'style': '{'},
        'simple': {'format': '{levelname} {message}', 'style': '{'},
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'casestudy.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'custom_admin_email': {
            'level': 'WARNING',
            'class': 'casestudies.logging_handlers.CustomAdminEmailHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console', 'custom_admin_email'],
            'level': 'DEBUG' if DEBUG else 'ERROR',
            'propagate': True,
        },
    },
}

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'mail.privateemail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'False').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

# Admin email configuration
ADMINS = [
    (os.environ.get('ADMIN_NAME', 'Mushfikur Rahman'), os.environ.get('ADMIN_EMAIL', 'mushfikurahmaan@gmail.com'))
]

# Production security settings
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'


# CKEditor 5 Configuration
customColorPalette = [
    {'color': 'hsl(4, 90%, 58%)', 'label': 'Red'},
    {'color': 'hsl(340, 82%, 52%)', 'label': 'Pink'},
    {'color': 'hsl(291, 64%, 42%)', 'label': 'Purple'},
    {'color': 'hsl(262, 52%, 47%)', 'label': 'Deep Purple'},
    {'color': 'hsl(231, 48%, 48%)', 'label': 'Indigo'},
    {'color': 'hsl(207, 90%, 54%)', 'label': 'Blue'},
    {'color': '#4285f2', 'label': 'Google Blue'},
    {'color': '#000000', 'label': 'Black'},
    {'color': '#ffffff', 'label': 'White'},
    {'color': 'hsl(142, 63%, 44%)', 'label': 'Green'},
    {'color': 'hsl(39, 100%, 50%)', 'label': 'Orange'},
    {'color': 'hsl(195, 100%, 40%)', 'label': 'Cyan'},
    {'color': 'hsl(30, 70%, 53%)', 'label': 'Amber'},
    {'color': 'hsl(260, 80%, 70%)', 'label': 'Lavender'},
    {'color': 'hsl(15, 85%, 65%)', 'label': 'Coral'},
]

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': {
            'items': ['heading', '|', 'bold', 'italic', 'link',
                      'bulletedList', 'numberedList', 'blockQuote', 'imageUpload'],
        }
    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],
        'toolbar': {
            'items': [
                'heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
                'code', 'subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
                'bulletedList', 'numberedList', 'todoList', '|', 'blockQuote', 'imageUpload', '|',
                'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                'insertTable',
            ],
            'shouldNotGroupWhenFull': 'true'
        },
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                        'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side', '|'],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]
        },
        'table': {
            'contentToolbar': [
                'tableColumn', 'tableRow', 'mergeTableCells',
                'tableProperties', 'tableCellProperties'
            ],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            }
        },
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1'},
                {'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2'},
                {'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3'}
            ]
        },
        'fontColor': {
            'colors': customColorPalette,
            'columns': 5,
            'default': '#000000'  # Default font color set to black
        },
        'ui': {
            'viewportOffset': {
                'top': 0,
                'bottom': 0
            }
        },'codeBlock': {
    'languages': [
        {'language': 'plaintext', 'label': 'Plain text'},
        {'language': 'bash', 'label': 'Bash'},
        {'language': 'python', 'label': 'Python'},
        {'language': 'javascript', 'label': 'JavaScript'},
        {'language': 'typescript', 'label': 'TypeScript'},
        {'language': 'html', 'label': 'HTML'},
        {'language': 'css', 'label': 'CSS'},
        {'language': 'json', 'label': 'JSON'},
        {'language': 'sql', 'label': 'SQL'},              # ✅ Ensure SQL is included
        {'language': 'java', 'label': 'Java'},
        {'language': 'c', 'label': 'C'},
        {'language': 'cpp', 'label': 'C++'},
        {'language': 'php', 'label': 'PHP'},
        {'language': 'xml', 'label': 'XML'},
        {'language': 'yaml', 'label': 'YAML'},
        {'language': 'dockerfile', 'label': 'Dockerfile'},
        {'language': 'powershell', 'label': 'PowerShell'},
        {'language': 'perl', 'label': 'Perl'},
        {'language': 'ruby', 'label': 'Ruby'},
        {'language': 'r', 'label': 'R'},
        {'language': 'go', 'label': 'Go'},
        {'language': 'swift', 'label': 'Swift'},
        {'language': 'kotlin', 'label': 'Kotlin'},
        {'language': 'markdown', 'label': 'Markdown'},
    ]
}

    },
    'list': {
        'properties': {
            'styles': 'true',
            'startIndex': 'true',
            'reversed': 'true',
        }
    }
}


# Define file upload permissions
CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"

EMAIL_TIMEOUT = int(os.environ.get('EMAIL_TIMEOUT', 20))
EMAIL_SUBJECT_PREFIX = os.environ.get('EMAIL_SUBJECT_PREFIX', '[Casestudies] ')
EMAIL_USE_LOCALTIME = os.environ.get('EMAIL_USE_LOCALTIME', 'True').lower() == 'true'
MANAGERS = [
    (os.environ.get('MANAGER_NAME', 'Manager'), os.environ.get('MANAGER_EMAIL', 'manager@casestudies.local'))
]
