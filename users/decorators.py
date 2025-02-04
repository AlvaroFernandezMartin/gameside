import json

from django.contrib.auth import get_user_model
from django.http import JsonResponse


def auth_required(func):
    def wrapper(request, *args, **kwargs):
        User = get_user_model()
        try:
            payload = json.loads(request.body)

            user = User.objects.get(token__key=payload.get('token'))

            request.user = user

        except User.DoesNotExist:
            return JsonResponse(
                {'error': 'Unknown authentication token'},
                status=401,
            )
        return func(request, *args, **kwargs)

    return wrapper
