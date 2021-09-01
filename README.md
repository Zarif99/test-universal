# docsie-universal-doc-importer
Python/Django library to import documentation from anywhere and send it to anywhere. Made by [Docsie](https://www.docsie.io).

The primary goal of this library is to serve as a universal interface for importing docs to your app. The idea here is to provide django developers with a familiar 
interface to build import/export modules for their app, so they no longer need to write their own code. 

We appretiate any help and support for this module and look forward to seeing your comments. 


## Current List of Adapters
- Github
- Gitlab
- Bitbucket


## Adapters on the roadmap
- Confluence
- Swaggerhub
- Google Drive
- Dropbox
- Box
- HTML
- S3
- Google Cloud Storage
- Azure Blob Storage


# Getting started

## Install

```bash
$ pip3 install git+https://github.com/LikaloLLC/docsie-universal-doc-importer
```

## Configurations
### 1. project_name/settings.py
```
INSTALLED_APPS = [
    ...
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
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.gitlab',
    'allauth.socialaccount.providers.bitbucket_oauth2',

    # encrypted model fields
    'encrypted_model_fields',

    # swag_auth
    'swag_auth',

    # universal importer
    'docsie_universal_importer.apps.DocsieUniversalImporterConfig'
    
    ...
]


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
            'key': 'bitbucket key',
            'secret': 'bitbucket secret',
        },
        'SCOPE': [
            'repository',
        ],
    },
    'github': {
        'APP': {
            'client_id': 'github client id',
            'secret': 'github secret',
        },
        'SCOPE': [
            'repo',
        ],
    },
    'gitlab': {
        'APP': {
            'client_id': 'gitlab client id',
            'secret': 'gitlab secret',
        },
        'SCOPE': [
            'read_repository',
            'api',
        ]
    }
}

FIELD_ENCRYPTION_KEY = 'field-encryption-key'
```

### 2. project_name/urls.py
```angular2html
    path('importer/', include('docsie_universal_importer.urls')),
    path('swag/', include('swag_auth.urls')),
    path('account/', include('rest_auth.urls'))
```
