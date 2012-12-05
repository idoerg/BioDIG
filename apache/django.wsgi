import os
import sys

path = '/var/www/mycoplasma_site'
otherpath = '/var/www'
sys.path.append(path)

sys.path.append(otherpath)

os.environ['DJANGO_SETTINGS_MODULE'] = 'mycoplasma_site.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

