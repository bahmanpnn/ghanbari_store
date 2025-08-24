from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%jl3&1t%-)^*feq)t9u-qdyckmfwo_bl1p*jzy!0ps^%)38x$u'
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-%jl3&1t%-)^*feq)t9u-qdyckmfwo_bl1p*jzy!0ps^%)38x$u")


DEBUG = os.environ.get("DEBUG_MODE",False)
ALLOWED_HOSTS = ["*"]

# ALLOWED_HOSTS = ["localhost", "127.0.0.1", "yourdomain.com"]
# ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# CSRF for Cookies
# CSRF_TRUSTED_ORIGINS = ["*"]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "http://127.0.0.1",
    # "https://yourdomain.com",
]



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # local apps
    'home_module.apps.HomeModuleConfig',
    'account_module.apps.AccountModuleConfig',
    'about_us_module.apps.AboutUsModuleConfig',
    'contact_module.apps.ContactModuleConfig',
    'product_module.apps.ProductModuleConfig',
    'blog_module.apps.BlogModuleConfig',
    'order_module.apps.OrderModuleConfig',
    'polls.apps.PollsConfig',
    'user_profile_module.apps.UserProfileModuleConfig',
    'site_settings_module.apps.SiteSettingsModuleConfig',
    'zarinpal_module.apps.ZarinpalModuleConfig',

    # third party packages
    'django_render_partial',
    'sorl.thumbnail',
    'jalali_date',
    'django_ckeditor_5',
    # 'ckeditor',
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

ROOT_URLCONF = 'ghanbari_store.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'order_module.context_processors.basket_products',
            ],
        },
    },
]

WSGI_APPLICATION = 'ghanbari_store.wsgi.application'


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'postgres',
#         'USER':'postgres',
#         'PASSWORD':'postgres',
#         'HOST':'ghanbari_store_postgres',
#         'PORT':'5432',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("POSTGRES_DB", "postgres"),
        'USER': os.environ.get("POSTGRES_USER", "postgres"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD", "postgres"),
        'HOST': os.environ.get("POSTGRES_HOST", "ghanbari_store_postgres"),
        'PORT':'5432',
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True



# Extra configs
STATIC_URL = "/static/"
STATIC_ROOT=BASE_DIR / "static_files"

STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL="/media_files/"
MEDIA_ROOT=BASE_DIR / "media_files"


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# User model configuration
AUTH_USER_MODEL='account_module.User'


CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|', 'bold', 'italic', 'underline', '|', 
            'alignment', 'fontFamily', 'fontSize', 'fontColor', 'fontBackgroundColor', '|', 
            'numberedList', 'bulletedList', '|', 
            'link', 'imageUpload', 'mediaEmbed', '|', 
            'undo', 'redo', '|', 'removeFormat', 'htmlEmbed','sourceEditing'
        ],
        'htmlSupport': {
            'allow': [
                {
                    'name': 'div',
                    'attributes': {
                        'class': True,  # Allow "class" attribute
                        'style': True,  # Allow "style" attribute
                    },
                    'styles': {
                        'color': True,  # Allow inline color styles
                        'background-color': True,
                    },
                },
                {
                    'name': 'span',
                    'attributes': {
                        'class': True,
                        'style': True,
                    },
                },
            ],
            'disallow': [
                {
                    'name': 'script',  # Disallow <script> tags for security
                },
            ],
        },
        'height': 300,
        'width': '100%',
        
    },
}



# Payment Gateway Configuration
# SANDBOX MODE
ZARINPAL_SANDBOX = True  # Set to False in production
ZARINPAL_MERCHANT_ID = "00000000-0000-0000-0000-000000000000"  # Sandbox merchant ID
ZARINPAL_CALLBACK_URL = "http://127.0.0.1:8000/zarinpal/verify/"
# MERCHANT="a9aea4fd-edb9-4ccf-bd62-170e87927e24" # testing uuid and its not valid merchant id


# Redis And Cache
# REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache", # Or "redis_cache.RedisCache" if using redis-py directly
        "LOCATION": f"redis://{REDIS_HOST}:6379/1", # Use the Redis service name defined in docker compose and redis host from env file
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# If using Redis for Celery broker and backend:
CELERY_BROKER_URL = f"redis://{REDIS_HOST}:6379/0"
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:6379/0"