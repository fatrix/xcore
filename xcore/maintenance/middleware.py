from django.http import HttpResponse
from django.conf import settings

import re

from utils import create_maintenance_file

class MaintenanceMiddleware:

    setting = "MAINTENANCE_ON"

    def __init__(self):
        """
        Recreate HTML file for maintenance mode.
        """
        create_maintenance_file()

    def process_request(self, request):
        mezzanine_maintenance = False
        try:
            from mezzanine.conf import settings as mezzanine_settings
            mezzanine_settings.use_editable()
            mezzanine_maintenance = getattr(mezzanine_settings, self.setting, False)
        except ImportError, e:
            pass

        if  mezzanine_maintenance == True or getattr(settings, self.setting, False):
            p = re.compile(r'.*(admin|media|__debug__|grappelli|maintenance)/.*')
            if not p.match(request.path):
                response = HttpResponseServiceUnavailable("Service Unavailable", mimetype="text/plain")
                return response
        return None

class HttpResponseServiceUnavailable(HttpResponse):
    status_code = 503

