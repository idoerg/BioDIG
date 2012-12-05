from django.db import connections

class DBRouter(object):
    """A router to control all database operations on models in
    the contrib.auth application"""

    def db_for_read(self, model, **hints):
        m = model.__module__.split('.')
        try:
            d = m[-1]
            if d in connections:
                return d
        except IndexError:
            pass
        return None

    def db_for_write(self, model, **hints):
        m = model.__module__.split('.')
        try:
            d = m[-1]
            if d in connections:
                return d
        except IndexError:
            pass
        return None

    def allow_syncdb(self, db, model):
        "Make sure syncdb doesn't run on anything but default"
        if model._meta.app_label == 'mycoplasma_home':
            return False
        elif db == 'default':
            return True
        return None

