"""
Django settings for bookmarks project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p5j#zzyaq)@ghzd#ug2=)!@dz%ixyym9i_u!+&e9&7h$1+-uhi'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# allowed hosts to enable authentication
ALLOWED_HOSTS = ['mysite.com', 'localhost', '127.0.0.1']
# ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'account.apps.AccountConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'django_extensions',
    'images.apps.ImagesConfig',
    'easy_thumbnails',
    
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bookmarks.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'bookmarks.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

#here  we kept the default ModelBackend that is used
# to authenticate with username and password and included our own
# email-based authentication backend.
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'account.authentication.EmailAuthBackend',
    # for facebook authentication
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.google.GoogleOAuth2'
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'


#################################login credentials
LOGIN_REDIRECT_URL = 'dashboard' #URL to redirect after a successful login if no next parameter is present in the request
LOGIN_URL = 'login' #The URL to redirect the user to log in
LOGOUT_URL = 'logout' #The URL to redirect the user to log out

'''For Django to serve media files uploaded by users with the
development server, add the following settings to the settings.py file
of your project:'''
# MEDIA_URL is the base URL to serve the media files uploaded by users,
MEDIA_URL = '/media/'
# MEDIA_ROOT is the local path where the images reside
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


SOCIAL_AUTH_FACEBOOK_KEY = '1258169217866367' #Facebook App ID
SOCIAL_AUTH_FACEBOOK_SECRET = '0eb27546e91e6178e7ec17f8d1e83fd3' #Facebook App Secret
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '500735434165-709g3vseascngkle8994um6sluf90nd6.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'zJI_nEXoZRB0L59HfpLe3u32'

'''Another way to specify the URL for a model except canonoical URL is by
adding the ABSOLUTE_URL_OVERRIDES setting to your project'''

# from django.urls import reverse_lazy

# ABSOLUTE_URL_OVERRIDES = {
#     'auth.user': lambda u: reverse_lazy('user_detail',
#                                         args=[u.username])
# }

'''Django adds a get_absolute_url() method dynamically to any models that appear
in the ABSOLUTE_URL_OVERRIDES setting. Now, you can use get_absolute_url() on a User instance to
retrieve its corresponding URL'''

from django.urls import reverse_lazy

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: reverse_lazy('user_detail',
                                        args=[u.username])
}