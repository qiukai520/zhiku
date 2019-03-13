"""
Django settings for thinking_library project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
from __future__ import absolute_import
import os
import redis
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 文件目录导入到搜索路径中
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')bc2g9%#4#c94i&!@_ll2l@f!@2_!u!f$y==+!7dnv4@5)y$$1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

AUTH_USER_MODEL = 'rbac.User'

AUTHENTICATION_BACKENDS = (
# 'django.contrib.auth.backends.ModelBackend',
# 'guardian.backends.ObjectPermissionBackend',
'rbac.views.CustomBackend',
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'task.apps.TaskConfig',
    'rbac.apps.RbacConfig',
    'personnel.apps.PersonnelConfig',
    'inventory.apps.InventoryConfig',
    'sfa.apps.SfaConfig',
    'public.apps.PublicConfig',
    'notice.apps.NoticeConfig',
    'article.apps.ArticleConfig',
    'contract.apps.ContractConfig',
    'collection.apps.CollectionConfig',
    'service.apps.ServiceConfig',
    'apps.file.apps.FileConfig',
    'apps.api.apps.ApiConfig',
    'xadmin',
    'crispy_forms',
    'reversion',
    'djcelery',
    'rest_framework',
    #'guardian',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rbac.middlewares.rbac.LoginMiddleware',
    # 'rbac.middlewares.rbac.RbacMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'thinking_library.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.media",
            ],
        },
    },
]

WSGI_APPLICATION = 'thinking_library.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'zhiku-v1',
        'USER': 'zhiku',
        'PASSWORD': 'Aa@zhiku886',
        # 'NAME': 'thinking_library',
        # 'USER': 'root',
        # 'PASSWORD': 'a741258963',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
        }

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


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

# LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'  # 设置静态文件的相对路径
STATIC_ROOT = os.path.join(BASE_DIR, "static_cdn")
MEDIA_URL = '/media/'  # 设置媒体文件的相对路径
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # 设置媒体文件的绝对路径

STATICFILES_DIRS = (
   os.path.join(BASE_DIR, 'static'),
   os.path.join(BASE_DIR, 'media'),
)

# LOGIN_URL = '/login/'




################## rbac配置 ###################

PERMISSION_URL_DICT_KEY = "permission_url_dict"
PERMISSION_MENU_KEY = "afsdfasdfadfsdfsdf"

VALID_URL = [
    "/login/",
    "/xadmin/*",
    "/logout/",
    "/article/",
    "/public/*",
    "/(\w+)/upload*",
    "/(\w+)/(\w+)/webuploader*",
    "/*notice*",
    "/*collection*",
    "/media/*",
    "/static/*",
]


# 缓存配置
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/0',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
             # "PASSWORD": "***",
        },
    },
}

# redis
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=1)
res = redis.Redis(connection_pool=pool)


# celery 配置信息
#############################
import djcelery
djcelery.setup_loader()
BROKER_URL = 'redis://127.0.0.1:6379/9'
CELERY_IMPORTS = ('task.tasks')
CELERY_TIMEZONE = 'Asia/Shanghai'

########################celery#######################

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']

from celery.schedules import timedelta
# 下面是定时任务的设置，我一共配置了三个定时任务.
from celery.schedules import crontab
CELERYBEAT_SCHEDULE = {
    # 定时任务一：　每24小时周期执行任务(daily_task)
    u'指派日常任务': {
        "task": "task.tasks.daily_task",
        "schedule": crontab(minute='*/2'),
        # "schedule":timedelta(seconds=5),
        "args": (),
    },
    # 定时任务二:　每周一的凌晨00:00分，执行任务(weekly_task)
    u'指派每周任务': {
        'task': 'task.tasks.weekly_task',
        'schedule': crontab(minute=0, hour=0,day_of_week="0"),
        # "schedule":timedelta(seconds=10),
        "args": ()
    },
    # 定时任务三:每个月的１号的00:00启动，执行任务(monthly_task)
    u'指派月任务': {
            'task': 'task.tasks.monthly_task',
            'schedule': crontab(hour=0, minute=0,   day_of_month='1'),
              # "schedule":timedelta(seconds=3),
            "args": ()
    },
    # 自动审核已完成任务:每30分钟执行一遍
    u'指派月任务': {
        'task': 'task.tasks.auto_task_review',
        'schedule': crontab(minute=30),
        # "schedule":timedelta(seconds=3),
        "args": ()
    },

    # 定时任务5：　每天凌晨检查客户列表()
    u'检查客户列表未成交客户': {
        "task": "sfa.tasks.check_customer",
        "schedule": crontab(hour=0, minute=0),
        # "schedule":timedelta(seconds=5),
        "args": (),
    },
}

#########################log#######################

from .logger import LOGGING

