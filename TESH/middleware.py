# TESH/middleware.py

class BypassTunnelMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Your middleware logic here
        return self.get_response(request)
