from django.utils import timezone
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect

class BlockCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            profile = getattr(request.user, 'profile', None)
            if profile and profile.is_currently_blocked():
                if profile.blocked_until:
                    date_str = profile.blocked_until.strftime('%d.%m.%Y %H:%M')
                    messages.error(request,
                                   f'Ваш аккаунт заблокирован до {date_str}')
                    logout(request)
                    return redirect('login')
        return self.get_response(request)