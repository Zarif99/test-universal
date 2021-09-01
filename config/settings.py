import os
from pathlib import Path

import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# Load operating system environment variables and then prepare to use them
env = environ.Env()
env_file = str(BASE_DIR / '.env')
env.read_env(env_file)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY', default='django-insecure-f^n19ezo)%ja=acz*$@)*$h4x*!4%0vr$-z_h4!pg)=vv1v9n*')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',

    # rest-framework apps
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',

    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # social accounts
    # 'allauth.socialaccount.providers.github',
    # 'allauth.socialaccount.providers.gitlab',
    # 'allauth.socialaccount.providers.bitbucket_oauth2',

    # drf yasg
    # 'drf_yasg',

    # encrypted model fields
    'encrypted_model_fields',

    # swag_auth
    'swag_auth',
    'swag_auth.github',
    'swag_auth.gitlab',
    'swag_auth.bitbucket',
    'swag_auth.box',
    'swag_auth.dropbox',
    'swag_auth.google_drive',
    'swag_auth.google_cloud_storage',

    'swag_auth.confluence',

    # universal importer
    'docsie_universal_importer.apps.DocsieUniversalImporterConfig',
    'docsie_universal_importer.providers.github',
    'docsie_universal_importer.providers.gitlab',
    'docsie_universal_importer.providers.bitbucket',
    'docsie_universal_importer.providers.box',
    'docsie_universal_importer.providers.dropbox',
    'docsie_universal_importer.providers.google_drive',
    'docsie_universal_importer.providers.google_cloud_storage',
    'docsie_universal_importer.providers.confluence',
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

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

SWAGAUTH_SETTINGS = {
    'bitbucket': {
        'APP': {
            'key': env.str('BITBUCKET_KEY'),
            'secret': env.str('BITBUCKET_SECRET'),
        },
        'SCOPE': [
            'repository',
        ],
    },
    'github': {
        'APP': {
            'client_id': env.str('GITHUB_CLIENT_ID'),
            'secret': env.str('GITHUB_SECRET'),
            'key': '',
        },
        'SCOPE': [
            'repo',
        ],
    },
    'gitlab': {
        'APP': {
            'client_id': env.str('GITLAB_CLIENT_ID'),
            'secret': env.str('GITLAB_SECRET'),
            'key': '',
        },
        'SCOPE': [
            'read_repository',
            'api',
        ]
    },
    'box': {
        'APP': {
            'client_id': env.str('BOX_CLIENT_ID'),
            'secret': env.str('BOX_SECRET'),
        },
        'SCOPE': [
            'root_readwrite'
        ],
    },
    'dropbox': {
        'APP': {
            'client_id': env.str('DROPBOX_CLIENT_ID'),
            'secret': env.str('DROPBOX_SECRET')
        },
        'SCOPE': [
            'files.content.read',
            'sharing.read',
        ]
    },
    'google': {
        'APP': {
            'client_id': env.str('GOOGLE_CLIENT_ID'),
            'secret': env.str('GOOGLE_SECRET'),
        },
        'SCOPE': [
            'email',
            'profile',
            'https://www.googleapis.com/auth/drive.readonly',
            'https://www.googleapis.com/auth/devstorage.read_only',
        ],
    },
    'google_cloud_storage': {
        'APP': {
            'client_id': env.str('GOOGLE_CLOUD_STORAGE_ID'),
            'secret': env.str('GOOGLE_CLOUD_STORAGE_SECRET'),
        },
        'SCOPE': [
            'https://www.googleapis.com/auth/devstorage.read_only',
        ],
    },
    'confluence': {
        'APP': {
            'client_id': env.str('CONFLUENCE_CLIENT_ID'),
            'secret': env.str('CONFLUENCE_SECRET'),
        },
        'SCOPE': [
            'read:confluence-content.summary',
            'read:confluence-space.summary',
            'read:confluence-props',
            'read:confluence-content.all',
            'read:confluence-user',
            'read:confluence-content.permission',
            'readonly:content.attachment:confluence'
        ],
    },
}

FIELD_ENCRYPTION_KEY = env('FIELD_ENCRYPTION_KEY')

UNIVERSAL_DOC_IMPORTER_SERIALIZER = 'docsie_universal_importer.adapter.ImportParamsSerializer'

# UNIVERSAL_DOC_IMPORTER_ADAPTER = 'docsie_universal_importer.adapter.MyImportAdapter'

UNIVERSAL_DOC_IMPORTER_PROVIDERS = {
    'github': {
        'import_adapter': 'docsie_universal_importer.adapter.MyImportAdapter'
    },
    'gitlab': {
        'import_adapter': 'docsie_universal_importer.adapter.MyImportAdapter'
    },
    'bitbucket': {
        'import_adapter': 'docsie_universal_importer.adapter.MyImportAdapter'
    },
    'box': {
        'import_adapter': 'docsie_universal_importer.adapter.MyImportAdapter'
    },
    'dropbox': {
        'import_adapter': 'docsie_universal_importer.adapter.MyImportAdapter'
    },
    'confluence': {
        'import_adapter': 'docsie_universal_importer.adapter.MyImportAdapter'
    },
    'google': {
        'import_adapter': 'docsie_universal_importer.adapter.MyImportAdapter'
    },
    'google_cloud_storage': {
        'import_adapter': 'docsie_universal_importer.adapter.MyImportAdapter'
    },
}
