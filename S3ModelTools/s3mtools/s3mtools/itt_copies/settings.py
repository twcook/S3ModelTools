"""
Django settings for Infotropic Tools project.
"""
import os
import configparser


# Setup config info
config = configparser.ConfigParser()
config.read('../itt.cfg')

ITTVERSION = config['SYSTEM']['version']


from unipath import Path

BASE_DIR = Path.cwd()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@ju_@vzo=vxfor&w@3&p5w!+kr*0(8@k)n($jm&gzq0+)x_ab^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: set the allowed hosts for production
ALLOWED_HOSTS = ['*']


if DEBUG:
    from fnmatch import fnmatch
    class glob_list(list):
        def __contains__(self, key):
            for elt in self:
                if fnmatch(key, elt): return True
            return False

    INTERNAL_IPS = glob_list(['127.0.0.1', '192.168.*.*'])



SITE_ID = 1

AUTH_USER_MODEL = 'auth.User'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'


# Application definition

INSTALLED_APPS = (
    'dal',
    'dal_select2',
    'dal_queryset_sequence',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'jquery',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'django_countries',
    'django_select2',
    'tastypie',
    'dmgen',
    'translator',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 180
CACHE_MIDDLEWARE_KEY_PREFIX = 'itt-'

ROOT_URLCONF = 'itt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
            ],
        },
    },
]


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)
ACCOUNT_EMAIL_VERIFICATION ='none'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True    # TODO: Set this to False for deployment.
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_MIN_LENGTH = 3

WSGI_APPLICATION = 'itt.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases


## development DB 
#DATABASES = {
    #'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'dmgen.db'),
    #}
#}


#   Production DB from config file
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dmgen',
        'USER': config['DATABASE']['user'],
        'PASSWORD': config['DATABASE']['password'],
        'HOST': config['DATABASE']['host'],
        'PORT': config['DATABASE']['port'],
    }

}

#DATABASES = {
    #'default': {
        #'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #'NAME': 'dmgen',
        #'USER': 'dctuser',
        #'PASSWORD': 'abcd1234',
        #'HOST': '127.0.0.1',
        #'PORT': '5432',
    #}

#}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = config['PREFS']['tz']

USE_I18N = True

USE_L10N = True

USE_TZ = True


# django_countries
COUNTRIES_FIRST = ['US', 'BR']
COUNTRIES_FIRST_REPEAT = True
COUNTRIES_FIRST_BREAK = '--'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = Path(BASE_DIR.parent, "static")
STATIC_URL = '/static/'

MEDIA_ROOT = Path(BASE_DIR.parent, "media")
DATA_LIB = Path(BASE_DIR.parent, "data")

# tastypie
TASTYPIE_FULL_DEBUG = True

TASTYPIE_DATETIME_FORMATTING = 'iso-8601'
API_LIMIT_PER_PAGE = 50
TASTYPIE_DEFAULT_FORMATS = ['json', 'xml', 'yaml']

# S3M settings
RMVERSION = config['SYSTEM']['s3mrm']
DM_LIB = Path(BASE_DIR.parent, "dmlib")
DM_PKG = Path(BASE_DIR.parent, "dmpkgs")
RM_URI = "https://www.s3model.com/ns/s3m/s3model_3_1_0.xsd"
RM_DIR = "../rm"
APPGEN_TEMPLATE_DIR = Path(BASE_DIR, "dmgen", "wc_modules", "appgen")
APPLIB_DIR = Path(BASE_DIR.parent, "applib")
