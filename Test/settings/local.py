from .base import *

DEBUG = True
ALLOWED_HOSTS = ["192.168.0.0/16", "127.0.0.1"]

SECRET_KEY = 'django-insecure-)3&nbjf!q)j)@ye-!$^4d8cl4!+qmlsqz_ac%ugvrnagiwa2w@'

LDAP_AUTH_URL = "ldap://192.168.1.189:389"
LDAP_AUTH_CONNECTION_USERNAME = "admin"
LDAP_AUTH_CONNECTION_PASSWORD = "123456"

INSTALLED_APPS += (
    # other apps for production site
)

CACHE_MIDDLEWARE_SECONDS = 300

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://192.168.1.189:6379',
        'TIMEOUT': 300,
        "OPTIONS": {
            'parser_class': 'redis.connection.PythonParser',
            'pool_class': 'redis.BlockingConnectionPool',
        }
    }
}

## 钉钉群的 WEB_HOOK， 用于发送钉钉消息
DINGTALK_WEB_HOOK = 'https://oapi.dingtalk.com/robot/send?access_token=cd10e38a8d810e8d27aba60949faf47afc6a6043b6158c537b7a016fd15ff1db'


import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="http://9f6860be335d4bf49b3c79769cde8e3b@192.168.1.189:9000/2",
    integrations=[
        DjangoIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

CELERY_BROKER_URL ="redis://192.168.1.189/0"
CELERY_REDIS_HOST="192.168.1.189"
CELERY_RESULT_BACKEND="redis://192.168.1.189/1"
CELERY_ACCEPT_CONTENT=['application/json']
CELERY_RESULT_SERIALIZER="json"
CELERY_TASK_SERIALIZER="json"
CELERY_TIMEZONE = "Asia/Shanghai"
CELERYD_MAX_TASKS_PER_CHILD=10
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERYD_LOG_FILE = os.path.join(BASE_DIR, "logs", "celery_work.log")
CELERYBEAT_LOG_FILE = os.path.join(BASE_DIR, "logs", "celery_beat.log")