import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class APICSRFExemptMiddleware(MiddlewareMixin):
    """
    Middleware that automatically exempts all '/api/' endpoints from Django's default CSRF checks.
    This eliminates the need to manually add @csrf_exempt decorators on every view/action in the API.
    """
    def process_request(self, request):
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)


class APILoggingMiddleware(MiddlewareMixin):
    """
    Middleware that logs incoming requests to '/api/' for monitoring and debugging.
    """
    def process_response(self, request, response):
        if request.path.startswith('/api/'):
            logger.info(f"API Request: {request.method} {request.path} -> Status: {response.status_code}")
        return response
