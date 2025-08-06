# Fichier : ql_django_app/settings.py (VERSION FINALE ET PROPRE)

from pathlib import Path
import os
# BASE_DIR pointe vers le dossier qui contient 'manage.py' (ql_django_app/)
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-apy5-j2n+2h_4kt5m=^3u8q4k%_8g&*^a5wa=g2mi%$fe_wi&*"
DEBUG = True
ALLOWED_HOSTS = []

# --- Application definition ---
# On ne liste que le strict minimum pour que l'application démarre
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "crispy_forms",
    "crispy_bootstrap4",

    # --- Applications de Catégories Actives ---
    'basics',
    'interest_rate_curves',
     'interest_rate_models',
      
    # --- Applications de Chapitres Actives ---
    # Ajoutez ici toutes les applications de chapitre que vous avez créées
    
    'chapter2_instruments',
    'chapter3_greeks',
    'chapter4_quotes',
    'chapter5_curves',
    'chapter6_pricing_range',
    'chapter7_random',
    'chapter10_treasury_curve',
    'chapter_eonia_curve',
    'chapter_euribor_curve',
    'chapter_day_count',
    'chapter_implied_curve',
    'chapter_glitch_curve',
    'chapter_sensitivities',
    'swap',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ql_django_app.urls"

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        
        # ==============================================================================
        # CORRECTION DÉFINITIVE ICI : On utilise os.path.join, qui est très robuste
        # ==============================================================================
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        
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

WSGI_APPLICATION = "ql_django_app.wsgi.application"
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}
AUTH_PASSWORD_VALIDATORS = [{"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},{"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},{"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},{"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"}]
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- Static files (CSS, JavaScript, Images) ---
STATIC_URL = "static/"
# Chemin vers votre dossier de fichiers statiques principal
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"