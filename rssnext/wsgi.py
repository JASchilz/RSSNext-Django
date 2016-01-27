"""
WSGI config for rssnext project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rssnext.settings")


def application(environ, start_response):
    os.environ.setdefault('DJANGO_CONFIGURATION', environ['DJANGO_CONFIGURATION'])

    from configurations.wsgi import get_wsgi_application

    return get_wsgi_application()(environ, start_response)
