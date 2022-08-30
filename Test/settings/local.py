from .base import *

ALLOWED_HOSTS = ["192.168.0.0/16", "127.0.0.1"]
LDAP_AUTH_CONNECTION_USERNAME = "admin"
LDAP_AUTH_CONNECTION_PASSWORD = "123456"

LDAP_AUTH_URL = "ldap://192.168.1.189:389"

SECRET_KEY = 'django-insecure-)3&nbjf!q)j)@ye-!$^4d8cl4!+qmlsqz_ac%ugvrnagiwa2w@'

DEBUG = True

INSTALLED_APPS += (
    
)