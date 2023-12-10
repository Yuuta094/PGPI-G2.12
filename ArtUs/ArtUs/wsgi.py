"""
WSGI config for artus project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ArtUs.settings')
application = get_wsgi_application()
application = WhiteNoise(application, root=os.path.join(settings.BASE_DIR, 'ArtUs', 'staticfiles'))

