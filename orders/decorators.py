import json
import re

from django.http import JsonResponse

from games.models import Game
from orders.models import Order
from users.models import Token


def check_token(view_func):
    """Verifica la autenticación del usuario a través del token."""

    def wrapped_view(request, *args, **kwargs):
        token_header = request.headers.get('Authorization')
        if not token_header:
            return JsonResponse({'error': 'Invalid authentication token'}, status=400)

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
    """Verifica que el usuario es dueño de la orden y la pasa a la vista."""

    def wrapped_view(request, *args, **kwargs):
        try:
            order = Order.objects.get(pk=kwargs['pk'])
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

        if request.user != order.user:
            return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)

        kwargs.pop('pk', None)

        return view_func(request, order=order, *args, **kwargs)

    return wrapped_view

def order_status(view_func):
    def wrapped_view(request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            status = data.get('status')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)
        if not status:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        
        return view_func(request,status=status,*args, **kwargs)
    return wrapped_view
def invalid_json(view_func):
    def wrapped_view(request, *args, **kwargs):
        try:
            body = json.loads(request.body)
            slug = body.get('game-slug')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)
        if not slug:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        return view_func(request, *args, **kwargs)

    return wrapped_view


def game_chequed(view_func):
    def wrapped_view(request, *args, **kwargs):
        try:
            order = Order.objects.get(pk=kwargs['pk'])
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        try:
            body = json.loads(request.body)
            slug = body.get('game-slug')
            game = Game.objects.get(slug=slug)
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found'}, status=404)
        

        if request.user != order.user:
            return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)

        kwargs.pop('pk', None)

        return view_func(request, order=order,game=game, *args, **kwargs)

    return wrapped_view
    
