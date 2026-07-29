import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class APICSRFExemptMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)


class APILoggingMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path.startswith('/api/'):
            logger.info(f"API Request: {request.method} {request.path} -> Status: {response.status_code}")
        return response

