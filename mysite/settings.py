"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path
import saml2
import saml2.saml

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-yp@g_0bm#l!l6jbsz$s@t-a6oi8wbe4o_p!&fxnlrp&5-24i)v"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "[::1]",
    ".pythonanywhere.com",
    ".compute.amazonaws.com",
    ".winebarrel.work",
    "10.0.3.45",
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "blog.apps.BlogConfig",
    "djangosaml2",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "djangosaml2.middleware.SamlSessionMiddleware",
]

SESSION_COOKIE_SECURE = True

ROOT_URLCONF = "mysite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'mysite', 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mysite.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "ja"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "/media/"
MEDIA_ROOT = Path(BASE_DIR / "media")

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    #"djangosaml2.backends.Saml2Backend",
    "lib.saml2.ModifiedSaml2Backend",
)

LOGIN_URL = "/saml2/login/"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

import saml2
SAML_DEFAULT_BINDING = saml2.BINDING_HTTP_POST

SAML_IGNORE_LOGOUT_ERRORS = True
# SAML2_DISCO_URL = "https://your.ds.example.net/"

SAML_DJANGO_USER_MAIN_ATTRIBUTE = "username" #emailAddress" #email"
#SAML_USE_NAME_ID_AS_USERNAME = True
SAML_CREATE_UNKNOWN_USER = True

# ACS_DEFAULT_REDIRECT_URL = reverse_lazy('some_url_name')

SAML_ATTRIBUTE_MAPPING = {
     "name": ("username",),
     "emailAddress": ("email",),
     "givenName": ("first_name",),
     "surname": ("last_name",),
}

LOGIN_REDIRECT_URL = '/admin'

SAML_CONFIG = {
    # full path to the xmlsec1 binary programm
    # "xmlsec_binary": "/usr/bin/xmlsec1",
    # your entity id, usually your subdomain plus the url to the metadata view
    "entityid": "https://django.winebarrel.work/saml2/acs/",
    # directory with attribute mapping
    # "attribute_map_dir": os.path.join(BASE_DIR, "attribute-maps"),
    # Permits to have attributes not configured in attribute-mappings
    # otherwise...without OID will be rejected
    #"allow_unknown_attributes": True,
    # this block states what services we provide
    "service": {
        # we are just a lonely SP
        "sp": {
            #"name": "Federated Django sample SP",
            #"name_id_format": saml2.saml.NAMEID_FORMAT_TRANSIENT,
            # For Okta add signed logout requests. Enable this:
            # "logout_requests_signed": True,
            "endpoints": {
                # url and binding to the assetion consumer service view
                # do not change the binding or service name
                "assertion_consumer_service": [
                    ("https://django.winebarrel.work/saml2/acs/", saml2.BINDING_HTTP_POST),
                ],
                # url and binding to the single logout service view
                # do not change the binding or service name
                "single_logout_service": [
                    # Disable next two lines for HTTP_REDIRECT for IDP's that only support HTTP_POST. Ex. Okta:
                    ("https://django.winebarrel.work/saml2/ls/", saml2.BINDING_HTTP_REDIRECT),
                    ("https://django.winebarrel.work/saml2/ls/post", saml2.BINDING_HTTP_POST),
                ],
            },
            #"signing_algorithm": saml2.xmldsig.SIG_RSA_SHA256,
            #"digest_algorithm": saml2.xmldsig.DIGEST_SHA256,
            # Mandates that the identity provider MUST authenticate the
            # presenter directly rather than rely on a previous security context.
            #"force_authn": False,
            # Enable AllowCreate in NameIDPolicy.
            #"name_id_format_allow_create": False,
            # attributes that this project need to identify a user
            #"required_attributes": ["givenName", "sn", "mail"],
            # attributes that may be useful to have but not required
            #"optional_attributes": ["eduPersonAffiliation"],
            "want_response_signed": False, #True,
            #"authn_requests_signed": False, #True,
            #"logout_requests_signed": False, #True,
            # Indicates that Authentication Responses to this SP must
            # be signed. If set to True, the SP will not consume
            # any SAML Responses that are not signed.
            #"want_assertions_signed": False, #True,
            #"only_use_keys_in_metadata": True,
            # When set to true, the SP will consume unsolicited SAML
            # Responses, i.e. SAML Responses for which it has not sent
            # a respective SAML Authentication Request.
            #"allow_unsolicited": True, #False,
            # in this section the list of IdPs we talk to are defined
            # This is not mandatory! All the IdP available in the metadata will be considered instead.
            # "idp": {
            #     # we do not need a WAYF service since there is
            #     # only an IdP defined here. This IdP should be
            #     # present in our metadata
            #     # the keys of this dictionary are entity ids
            #     "https://localhost/simplesaml/saml2/idp/metadata.php": {
            #         "single_sign_on_service": {
            #             saml2.BINDING_HTTP_REDIRECT: "https://localhost/simplesaml/saml2/idp/SSOService.php",
            #         },
            #         "single_logout_service": {
            #             saml2.BINDING_HTTP_REDIRECT: "https://localhost/simplesaml/saml2/idp/SingleLogoutService.php",
            #         },
            #     },
            # },
        },
    },
    # where the remote metadata is stored, local, remote or mdq server.
    # One metadatastore or many ...
    "metadata": {
        # "local": [os.path.join(BASE_DIR, "remote_metadata.xml")],
        "remote": [
            {"url": "https://login.microsoftonline.com/xxx/federationmetadata/2007-06/federationmetadata.xml?appid=xxx"},
        ],
        # "mdq": [
        #     {
        #         "url": "https://ds.testunical.it",
        #         "cert": "certficates/others/ds.testunical.it.cert",
        #     }
        # ],
    },
    # set to 1 to output debugging information
    "debug": 1,
    # Signing
    #"key_file": os.path.join(BASE_DIR, "server.key"),  # private part
    #"cert_file": os.path.join(BASE_DIR, "server.crt"),  # public part
    # Encryption
    #"encryption_keypairs": [
    #    {
    #        "key_file": os.path.join(BASE_DIR, "server.key"),  # private part
    #        "cert_file": os.path.join(BASE_DIR, "server.crt"),  # public part
    #    }
    #],
    # own metadata settings
    # "contact_person": [
    #     {
    #         "given_name": "Lorenzo",
    #         "sur_name": "Gil",
    #         "company": "Yaco Sistemas",
    #         "email_address": "lorenzo.gil.sanchez@gmail.com",
    #         "contact_type": "technical",
    #     },
    #     {
    #         "given_name": "Angel",
    #         "sur_name": "Fernandez",
    #         "company": "Yaco Sistemas",
    #         "email_address": "angel@yaco.es",
    #         "contact_type": "administrative",
    #     },
    # ],
    # you can set multilanguage information here
    # "organization": {
    #     "name": [("Yaco Sistemas", "es"), ("Yaco Systems", "en")],
    #     "display_name": [("Yaco", "es"), ("Yaco", "en")],
    #     "url": [("http://www.yaco.es", "es"), ("http://www.yaco.com", "en")],
    # },
}
