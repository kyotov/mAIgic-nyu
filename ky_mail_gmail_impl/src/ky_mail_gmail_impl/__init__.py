import ky_mail_api

from . import _impl

# Dependency Injection of this implementation into the API
#
ky_mail_api.get_client = lambda: _impl.Client()
