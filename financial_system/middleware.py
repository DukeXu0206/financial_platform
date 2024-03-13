# yourapp/middleware.py
from django.contrib.auth import get_user
from django.contrib.auth.models import AnonymousUser

class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 从session中获取用户信息
        request.current_user = request.user if request.user.is_authenticated else None
        response = self.get_response(request)

        return response
