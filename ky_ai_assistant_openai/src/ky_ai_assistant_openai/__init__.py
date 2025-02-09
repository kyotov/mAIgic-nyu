import ky_ai_assistant_api

from . import _impl

# Dependency Injection of this implementation into the API
#
ky_ai_assistant_api.get_client = lambda: _impl.Client()
