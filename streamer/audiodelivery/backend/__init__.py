from django.utils.translation import gettext_lazy as _

from audiodelivery.utils.importer import import_module_from_string

from audiodelivery.settings import BACKENDS


def get_backend(typo):

    backend_path = BACKENDS[typo]

    backend = import_module_from_string(backend_path)

    if backend is None:
        raise ModuleNotFoundError(_("Module %(path)s not found") % {"path": backend_path})
    
    return backend


def get_uplader_backend():
    return get_backend("upload")

def get_deliver_backend():
    return get_backend("deliver")