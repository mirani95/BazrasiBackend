from .models import BlacklistedAccessToken
from apps.authentication.tools import get_token_jti
from django.http import JsonResponse


class BlockedTokenMiddleware:
    """ Check blocked access token authentication """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token_str = auth_header[7:]
            jti, _ = get_token_jti(token_str)
            if jti and BlacklistedAccessToken.objects.filter(jti=jti).exists():
                return JsonResponse({
                    'detail': 'Access token has been blacklisted'
                }, status=401)

        return self.get_response(request)
