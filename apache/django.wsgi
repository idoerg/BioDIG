import os
import sys

path = '/var/www/BioDIG'
otherpath = '/var/www'
sys.path.append(path)

sys.path.append(otherpath)

os.environ['DJANGO_SETTINGS_MODULE'] = 'BioDIG.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

