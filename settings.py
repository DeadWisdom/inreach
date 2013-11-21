"""
Common settings.
"""
from os.path import abspath, basename, dirname, join, normpath, exists
from sys import path


##### Secrets #####
### Django Social Auth
# See: http://django-social-auth.readthedocs.org/en/latest/configuration.html#keys-and-secrets
TWITTER_CONSUMER_KEY         = NotImplementedError
TWITTER_CONSUMER_SECRET      = NotImplementedError

### Secret Key
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = NotImplementedError

### Load Secrets ###
from secrets import *



### Django Oauth Redirect ###
LOGIN_REDIRECT_URL = '/'


### DEBUG ###
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
#      https://docs.djangoproject.com/en/dev/ref/settings/#template-debug       
DEBUG = True
TEMPLATE_DEBUG = DEBUG


### APP ###
# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = (
    # Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',

    # Apps
    'social_auth',
    'app',
)


### URL ###
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'urls'


### MANAGER ###
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
ADMINS = MANAGERS = (
    ('Brantley Harris', 'deadwisdom@gmail.com')
)


### PATH ###
# Absolute filesystem path to the Django project directory:
ROOT = dirname(dirname(abspath(__file__)))


### DATABASE ###
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sqlite.db'
    }
}


### MEDIA ###
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(ROOT, 'media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'


### STATIC FILE ###
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(ROOT, 'static'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'


### LOCATION ###
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'America/Chicago'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True


### TEMPLATE ###
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',

    'social_auth.context_processors.social_auth_by_name_backends',
    'social_auth.context_processors.social_auth_backends',
    'social_auth.context_processors.social_auth_by_type_backends',
    'social_auth.context_processors.social_auth_login_redirect',
)

TWITTER_EXTRA_DATA = ['profile_image_url', 'screen_name']


### AUTHENTICATION ###
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_auth.backends.twitter.TwitterBackend',
)


### LOGGING ###
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging ###. The only tangible logging
# performed by this ### is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging ###.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'discourse':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    }
}


### WSGI ###
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'wsgi.application'

