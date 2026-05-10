from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "change-me-in-production"
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "django.contrib.sessions",
    "chat",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {}  # Pas de base Django — on utilise directement aplusSurLeau.db via SQLite

STATIC_URL = "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Chemin vers la base SQLite AplusSurLeau (à la racine du repo)
APLUSURLEAU_DB = BASE_DIR.parent / "aplusSurLeau.db"

# Clé API Anthropic — à définir en variable d'environnement
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
