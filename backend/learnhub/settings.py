import os
from pathlib import Path
from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition
DJANGO_APPS = [
    'jazzmin',  # Must be before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'channels',
    'django_filters',
    'storages',
    'import_export',
    'debug_toolbar',
    'silk',
    'cleanup',
    'widget_tweaks',
    'bootstrap4',
    'colorfield',
]

LOCAL_APPS = [
    'accounts',
    'courses',
    'payments',
    'mobile_payments',
    'analytics',
    'notifications',
    'dashboard',
    'zambian_education',  # New app for Zambian education system
    'ecz_papers',  # ECZ examination papers
    'online_classes',  # Live online classes
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_ratelimit.middleware.RatelimitMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'silk.middleware.SilkyMiddleware',
]

ROOT_URLCONF = 'learnhub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'learnhub.wsgi.application'
ASGI_APPLICATION = 'learnhub.asgi.application'

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='sqlite:///db.sqlite3')
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lusaka'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}

# JWT Configuration
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True

# Security Settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Session Security
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = True

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# Celery Configuration
CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6379/0')

# Channels Configuration
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [config('REDIS_URL', default='redis://localhost:6379/0')],
        },
    },
}

# AWS S3 Configuration (Optional)
USE_S3 = config('USE_S3', default=False, cast=bool)
if USE_S3:
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Stripe Configuration
STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY', default='')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default='')
STRIPE_WEBHOOK_SECRET = config('STRIPE_WEBHOOK_SECRET', default='')

# Mobile Money Configuration
MOBILE_MONEY_SETTINGS = {
    'AIRTEL_MERCHANT_CODE': config('AIRTEL_MERCHANT_CODE', default='LEARNHUB001'),
    'ZAMTEL_BUSINESS_NUMBER': config('ZAMTEL_BUSINESS_NUMBER', default='2001'),
    'MTN_PAYEE_CODE': config('MTN_PAYEE_CODE', default='LEARN001'),
    'SMS_PROVIDER': config('SMS_PROVIDER', default='africas_talking'),
    'PAYMENT_TIMEOUT_MINUTES': config('PAYMENT_TIMEOUT_MINUTES', default=30, cast=int),
    'SMS_API_KEY': config('SMS_API_KEY', default=''),
    'SMS_USERNAME': config('SMS_USERNAME', default=''),
}

# Zambian Education System Configuration
ZAMBIAN_EDUCATION_SETTINGS = {
    'ECZ_API_BASE_URL': config('ECZ_API_BASE_URL', default='https://api.ecz.gov.zm/v1/'),
    'ECZ_API_KEY': config('ECZ_API_KEY', default=''),
    'MOE_API_BASE_URL': config('MOE_API_BASE_URL', default='https://api.moe.gov.zm/v1/'),
    'MOE_API_KEY': config('MOE_API_KEY', default=''),
    'CURRICULUM_STANDARDS': {
        'PRIMARY': ['Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6', 'Grade 7'],
        'SECONDARY': ['Grade 8', 'Grade 9', 'Grade 10', 'Grade 11', 'Grade 12'],
        'SUBJECTS': {
            'PRIMARY': ['English', 'Mathematics', 'Science', 'Social Studies', 'Creative Arts', 'Physical Education', 'Local Languages'],
            'SECONDARY': ['English', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 'Geography', 'History', 'Civic Education', 'Religious Education', 'Computer Studies', 'Business Studies', 'Accounting', 'Economics']
        }
    },
    'ECZ_EXAMINATION_LEVELS': ['Grade 7', 'Grade 9', 'Grade 12'],
    'ACADEMIC_CALENDAR': {
        'TERM_1': {'start': '01-15', 'end': '04-15'},
        'TERM_2': {'start': '05-01', 'end': '08-15'},
        'TERM_3': {'start': '09-01', 'end': '12-15'}
    }
}

# Debug Toolbar Configuration
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

# Enhanced Jazzmin Configuration for Zambian Education Platform
JAZZMIN_SETTINGS = {
    "site_title": "EduZambia Admin",
    "site_header": "EduZambia - Zambian Education Platform",
    "site_brand": "EduZambia",
    "site_logo": "images/zambia-education-logo.png",
    "login_logo": "images/zambia-education-logo.png",
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": "images/zambia-flag-icon.ico",
    "welcome_sign": "Welcome to EduZambia Administration",
    "copyright": "Ministry of Education - Republic of Zambia",
    "search_model": ["accounts.User", "courses.Course", "ecz_papers.ECZPaper"],
    "user_avatar": None,
    
    # Top Menu
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Dashboard", "url": "/admin/dashboard/", "permissions": ["auth.view_user"]},
        {"name": "ECZ Papers", "url": "/admin/ecz_papers/", "permissions": ["auth.view_user"]},
        {"name": "Online Classes", "url": "/admin/online_classes/", "permissions": ["auth.view_user"]},
        {"name": "Analytics", "url": "/admin/analytics/", "permissions": ["auth.view_user"]},
        {"model": "accounts.User"},
        {"app": "courses"},
    ],

    # User Menu on the right side
    "usermenu_links": [
        {"name": "ECZ Portal", "url": "https://ecz.gov.zm", "new_window": True},
        {"name": "Ministry of Education", "url": "https://moe.gov.zm", "new_window": True},
        {"model": "accounts.user"}
    ],

    # Side Menu
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["accounts", "zambian_education", "ecz_papers", "courses", "online_classes", "payments", "analytics"],

    # Icons with Zambian education theme
    "icons": {
        "accounts": "fas fa-users-cog",
        "accounts.user": "fas fa-user-graduate",
        "accounts.Group": "fas fa-users",
        "zambian_education": "fas fa-school",
        "zambian_education.school": "fas fa-building",
        "zambian_education.grade": "fas fa-layer-group",
        "zambian_education.subject": "fas fa-book-open",
        "ecz_papers": "fas fa-file-alt",
        "ecz_papers.eczpaper": "fas fa-scroll",
        "ecz_papers.pastpaper": "fas fa-history",
        "courses": "fas fa-graduation-cap",
        "courses.course": "fas fa-chalkboard-teacher",
        "courses.category": "fas fa-tags",
        "courses.enrollment": "fas fa-user-graduate",
        "online_classes": "fas fa-video",
        "online_classes.liveclass": "fas fa-broadcast-tower",
        "payments": "fas fa-credit-card",
        "mobile_payments": "fas fa-mobile-alt",
        "analytics": "fas fa-chart-line",
        "notifications": "fas fa-bell",
    },

    # UI Tweaks with Zambian colors
    "custom_links": {
        "zambian_education": [{
            "name": "ECZ Syllabus", 
            "url": "ecz_syllabus", 
            "icon": "fas fa-book",
            "permissions": ["zambian_education.view_subject"]
        }]
    },
    "use_google_fonts_cdn": True,
    "show_ui_builder": True,

    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"accounts.user": "collapsible", "accounts.group": "vertical_tabs"},
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-success",  # Green for Zambian flag
    "accent": "accent-success",
    "navbar": "navbar-success navbar-dark",  # Zambian green
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-success",  # Zambian theme
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-success",  # Zambian green
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": True
}

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'eduzambia.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'zambian_education': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'ecz_papers': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'online_classes': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Create logs directory
os.makedirs(BASE_DIR / 'logs', exist_ok=True)