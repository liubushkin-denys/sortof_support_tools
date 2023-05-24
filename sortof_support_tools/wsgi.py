"""
WSGI config for sortof_support_tools project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

path = "/home/dlsuppto/django-apps/sortof_support_tools"
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sortof_support_tools.settings')

application = get_wsgi_application()
