import os
import sys

path = 'E:\django\Portal'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'Portal.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
