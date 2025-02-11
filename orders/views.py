import json
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from games.models import Game
from games.Serializers.GameSerializer import GameSerializer
from shared.decorators import get_required, post_required

from .decorators import check_token, owner_order
from .models import Order
from .OrderSerializer import OrderSerializer


@csrf_exempt
@post_required
@check_token
def add_order(request):
    """Crea una nueva orden para el usuario autenticado."""
    order = Order.objects.create(
        status=Order.Status.INITIATED,
        user=request.user,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    return JsonResponse({'id': order.pk}, status=200)


@csrf_exempt
@get_required
@check_token
@owner_order
def order_detail(request, order):
    """Devuelve los detalles de una orden específica."""
    serializer = OrderSerializer(order, request=request)
    return serializer.json_response()


@csrf_exempt
@get_required
@check_token
@owner_order
def order_game_list(request, order):
    """Devuelve la lista de juegos en una orden específica."""
    games = order.games.all()
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


@csrf_exempt
@post_required
@check_token
@owner_order
def add_game_to_order(request, order):
    """Añade un juego a la orden si el usuario es dueño de la misma."""
    try:
        body = json.loads(request.body)
        slug = body.get('game-slug')
        if not slug:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        game = Game.objects.get(slug=slug)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)

    order.games.add(game)

    games_count = order.games.count()
    print(f'Order ID: {order.pk}, User: {order.user}, Game Slug: {game.slug}, Games Count: {games_count}')

    return JsonResponse({'num-games-in-order': games_count}, status=200)


@csrf_exempt
@post_required
@check_token
@owner_order
def change_order_status(request, order):
    """Cambia el estado de la orden si cumple con las condiciones de validación."""
    try:
        data = json.loads(request.body)
        status = data.get('status')
        if status not in [Order.Status.CONFIRMED, Order.Status.CANCELLED]:
            return JsonResponse({'error': 'Invalid status'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    if order.status != Order.Status.INITIATED:
        return JsonResponse(
            {'error': 'Orders can only be confirmed/cancelled when initiated'}, status=400
        )

    order.status = status
    order.save()

    if status == Order.Status.CANCELLED:
        for game in order.games.all():
            game.stock += 1
            game.save()

    return JsonResponse({'status': order.status, 'status_label': order.get_status_display()}, status=200)