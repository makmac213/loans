from django.conf import settings

class NonRelRouter(object):

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """

        ret = None
        if model._meta.module_name in settings.MODULES_NON_REL:
            ret = settings.DB_NONREL
        return ret

    #def db_for_write(self, model, **hints):
    #    """
    #    Attempts to read auth models go to auth_db.
    #    """
    #   
    #    ret = None
    #    if model._meta.module_name in settings.MODULES_NON_REL:
    #        ret = settings.DB_NONREL
    #    return ret
    #
    #def allow_relation(self, model, **hints):
    #    """
    #    Attempts to read auth models go to auth_db.
    #    """
    #    
    #    ret = None
    #    if model._meta.module_name in settings.MODULES_NON_REL:
    #        ret = settings.DB_NONREL
    #    return ret
    #

    def allow_syncdb(self, db, model):
        
        ret = True
        if model._meta.module_name in settings.MODULES_NON_REL:
            ret = False
        return ret


    # django 1.7.1
    #def allow_migrate(self, db, model):
    #    """
    #    Attempts to read auth models go to auth_db.
    #    """
    #    
    #    ret = True
    #    if model._meta.model_name in settings.MODULES_NON_REL:
    #        ret = False
    #    return ret
