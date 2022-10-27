"""
WSGI config for locallibrary project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""
##wsgi.py используется для налаживания связи между вашим Django приложением
##и веб-сервером. Вы можете воспринимать его, как утилиту.


import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'locallibrary.settings')

application = get_wsgi_application()
