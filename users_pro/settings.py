from pathlib import Path
import os
import environ
from datetime import timedelta
import pymysql

# ------------------------------
# BASE DIR
# ------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------
# Environment variables
# ------------------------------
env = environ.Env()
# read .env file if present (local) - in Render you set env vars in dashboard
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# ------------------------------
# SECURITY
# ------------------------------
SECRET_KEY = env('SECRET_KEY', default='replace-this-in-prod')
# env.bool will parse "True"/"False" strings too
DEBUG = env.bool('DEBUG', default=True)

# ------------------------------
# Allowed Hosts (use env var)
# ------------------------------
# Set DJANGO_ALLOWED_HOSTS="vechilebackend-9.onrender.com,localhost,127.0.0.1"
allowed_hosts_env = env('DJANGO_ALLOWED_HOSTS', default='localhost,127.0.0.1')
ALLOWED_HOSTS = [h.strip() for h in allowed_hosts_env.split(',') if h.strip()]

# ------------------------------
# Installed Apps
# ------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'corsheaders',

    # Your apps
    'users_app',
]

# ------------------------------
# Middleware
# ------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # must be above CommonMiddleware
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
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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
AUTH_USER_MODEL = 'users_app.userReg'

# ------------------------------
# Database (MySQL)
# ------------------------------
pymysql.install_as_MySQLdb()
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME', default='userDb'),
        'USER': env('DB_USER', default='root'),
        'PASSWORD': env('DB_PASSWORD', default=''),
        'HOST': env('DB_HOST', default='127.0.0.1'),
        'PORT': env('DB_PORT', default='3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# ------------------------------
# Password Validators
# ------------------------------
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
TIME_ZONE = 'Asia/Kolkata'   # set to your timezone
USE_I18N = True
USE_TZ = True

# ------------------------------
# Static Files
# ------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------------------
# Django REST Framework + JWT
# ------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# ------------------------------
# CORS (add deployed frontend origin too)
# ------------------------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
# If your frontend is deployed e.g. https://myfrontend.com add it:
# CORS_ALLOWED_ORIGINS.append("https://myfrontend.com")
CORS_ALLOW_CREDENTIALS = True

# ------------------------------
# SIMPLE_JWT Settings
# ------------------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'USER_ID_FIELD': 'userId',
    'USER_ID_CLAIM': 'user_id',
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# ------------------------------
# Proxy / SSL (if behind proxy like Render)
# ------------------------------
# Uncomment if your host sets X-Forwarded-Proto
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# USE_X_FORWARDED_HOST = True
