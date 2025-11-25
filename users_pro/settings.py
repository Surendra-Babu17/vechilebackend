from pathlib import Path
import os
import environ
from datetime import timedelta
import pymysql

# ------------------------------
# BASE DIR
# ------------------------------
# Django project root path define cheyyadam
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------
# Environment variables
# ------------------------------
# .env file nundi sensitive info (SECRET_KEY, DB details) read cheyyadam
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# ------------------------------
# SECURITY
# ------------------------------
# SECRET_KEY -> Django secret key (production lo strong ga pettali)
SECRET_KEY = env('SECRET_KEY', default='replace-this-in-prod')
# DEBUG -> Development mode on/off
DEBUG = env.bool('DEBUG', default=True)

# ------------------------------
# Allowed Hosts
# ------------------------------
# DEBUG = True -> localhost lo matrame allowed
# DEBUG = False -> production domain lo allow cheyyali
if DEBUG:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
else:
    ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['your-production-domain.com'])

# ------------------------------
# Installed Apps
# ------------------------------
INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',     # Django REST API framework
    'corsheaders',        # Cross-Origin Resource Sharing (frontend integration ki)

    # Custom apps
    'users_app',          # me app
]

# ------------------------------
# Middleware
# ------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # React frontend to allow cheyyali
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ------------------------------
# URLs & Templates
# ------------------------------
ROOT_URLCONF = 'users_pro.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Custom templates folder
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

WSGI_APPLICATION = 'users_pro.wsgi.application'

# ------------------------------
# Custom User Model
# ------------------------------
# me custom user model use cheyyali
AUTH_USER_MODEL = 'users_app.userReg'

# ------------------------------
# Database (MySQL)
# ------------------------------
# pymysql -> MySQL Python driver
pymysql.install_as_MySQLdb()
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME', default='userDb'),
        'USER': env('DB_USER', default='root'),
        'PASSWORD': env('DB_PASSWORD', default='Haritha#17'),
        'HOST': env('DB_HOST', default='127.0.0.1'),
        'PORT': env('DB_PORT', default='3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",  # MySQL strict mode
        },
    }
}

# ------------------------------
# Password Validators
# ------------------------------
# Django default validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# ------------------------------
# Internationalization
# ------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ------------------------------
# Static Files
# ------------------------------
STATIC_URL = '/static/'                 # URL lo static files access
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Production lo collectstatic folder

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------------------
# Django REST Framework + JWT
# ------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT token auth
    ),
}

# ------------------------------
# CORS (Frontend + Backend integration)
# ------------------------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React local dev server
]
CORS_ALLOW_CREDENTIALS = True      # Cookies send cheyyali

# ------------------------------
# SIMPLE_JWT Settings
# ------------------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),      # Access token valid time
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),         # Refresh token valid time
    'USER_ID_FIELD': 'userId',                            # me custom user primary key
    'USER_ID_CLAIM': 'user_id',
    'ROTATE_REFRESH_TOKENS': True,                        # refresh rotate
    'BLACKLIST_AFTER_ROTATION': True,                     # refresh token blacklist
}
