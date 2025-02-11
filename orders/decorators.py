import re

from django.http import JsonResponse

from orders.models import Order
from users.models import Token


def check_token(view_func):
    def wrapped_view(request, *args, **kwargs):
        token_header = request.headers.get('Authorization')
        if not token_header:
            return JsonResponse(
                {'error': 'Invalid authentication token'}, status=400
            )  # Corregido aquí

        match = re.fullmatch(
            r'Bearer (?P<token_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12})',
            token_header,
        )

        if not match:
            return JsonResponse({'error': 'Invalid authentication token'}, status=400)

        token_str = match.group('token_id')
        try:
            token_obj = Token.objects.get(key=token_str)
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Unregistered authentication token'}, status=401)

        request.user = token_obj.user

        return view_func(request, *args, **kwargs)

    return wrapped_view


def owner_order(view_func):
    def wrapped_view(request, *args, **kwargs):
        try:
            order = Order.objects.get(pk=kwargs['pk'])
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

        if request.user != order.user:
            return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)

        return view_func(request, *args, **kwargs)

    return wrapped_view
