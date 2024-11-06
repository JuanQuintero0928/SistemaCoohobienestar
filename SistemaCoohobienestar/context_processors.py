# context_processors.py
from django.conf import settings

def session_timeout(request):
    return {
        'session_timeout': settings.SESSION_COOKIE_AGE
    }
