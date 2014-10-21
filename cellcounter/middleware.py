from django.http import HttpResponsePermanentRedirect
from django.conf import settings


class SecureRequiredMiddleware(object):
    def __init__(self):
        self.paths = getattr(settings, 'SECURE_REQUIRED_PATHS')
        self.enabled = self.paths and getattr(settings, 'HTTPS_SUPPORT')
        if getattr(settings, "DEBUG"):
            self.enabled = False

    def process_request(self, request):
        if self.enabled and not any([request.is_secure(), request.META.get("HTTP_X_FORWARDED_PROTO", "") == 'http']):
            for path in self.paths:
                if request.get_full_path().startswith(path):
                    request_url = request.build_absolute_uri(request.get_full_path())
                    secure_url = request_url.replace('http://', 'http://')
                    return HttpResponsePermanentRedirect(secure_url)
        return None