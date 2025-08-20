import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECURITY_KEY", default="unsafe-secret-key-change-me")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"

ALLOWED_HOSTS = ['*']

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

OUR_APPS = [
    'user_accounts',
    'cart.apps.CartConfig',
    'orders.apps.OrdersConfig',
    'products.apps.ProductsConfig',
    'api.apps.ApiConfig',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'django_filters',
    'rest_framework.authtoken',
    'drf_spectacular',
    'django_cleanup.apps.CleanupConfig',
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
]

INSTALLED_APPS = DJANGO_APPS + OUR_APPS + THIRD_PARTY_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware'
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "drf_db_ecommerce"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "01712062236"),
        "HOST": os.getenv("POSTGRES_HOST", "db"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}



# Custom User
AUTH_USER_MODEL = 'user_accounts.CustomUser'

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'


# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # default works if USERNAME_FIELD=email
]


# Email-only login
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1", "password2", "first_name", "last_name"]
ACCOUNT_EMAIL_VERIFICATION = "none"



# REST Framework + dj-rest-auth
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# django-allauth (email only)
# Email-only login
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "none"

# dj-rest-auth serializers
REST_AUTH = {
    "REGISTER_SERIALIZER": "user_accounts.serializers.CustomRegistrationSerializer",
    'LOGIN_SERIALIZER': 'user_accounts.serializers.CustomLoginSerializer',
    'USER_DETAILS_SERIALIZER': 'user_accounts.serializers.UserSerializer',
    'OLD_PASSWORD_FIELD_ENABLED': True,
}


SPECTACULAR_SETTINGS = {
    # Basic metadata
    'TITLE': 'Glovendar E-commerce API',
    'DESCRIPTION': (
        "Glovendar is a modern e-commerce platform API. "
        "It provides endpoints for managing products, categories, carts, "
        "user authentication, and order processing. "
        "Designed for fast, secure, and scalable integrations."
    ),
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': True,  # Serve schema via /api/schema/ endpoint

    # OpenAPI specifics
    'SCHEMA_PATH_PREFIX': r'/api/',  # Only include paths starting with /api/
    'COMPONENT_SPLIT_REQUEST': True,  # Split request and response schemas
    'COMPONENT_SPLIT_PATCH': True,    # Separate PATCH from PUT
    'COMPONENT_NO_READ_ONLY_REQUIRED': False,  # Read-only fields are not required in request
    'ENUM_NAME_OVERRIDES': {},

    # Authentication
    'SECURITY': [{'TokenAuth': []}],  # For TokenAuth (adjust if using JWT or OAuth)
    
    # Optional: Add tags for better grouping
    'TAGS': [
        {
            'name': 'Products',
            'description': 'Manage products, categories, and inventory.'
        },
        {
            'name': 'Cart',
            'description': 'Endpoints for managing user and guest shopping carts.'
        },
        {
            'name': 'Orders',
            'description': 'Endpoints for creating and managing orders.'
        },
    ],

    # Optional: Default server info
    # 'SERVERS': [
    #     {'url': 'http://localhost:8000', 'description': 'Development server'},
    #     {'url': 'https://api.glovendar.enghasan.com', 'description': 'Production server'}
    # ],

    # Optional: Auto tags endpoints based on ViewSet or router
    'AUTO_TAGS': 'list',  

    # Optional: Customize schema output formatting
    'SORT_OPERATIONS': True,
    'TITLE_OVERRIDE': 'Glovendar E-Commerce API',
}


SITE_ID = 1




EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True