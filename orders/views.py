import json,re,datetime
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from games.Serializers.GameSerializer import GameSerializer
from shared.decorators import get_required, post_required

from .decorators import check_token, game_chequed, invalid_json, owner_order,order_status,check_card
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
@invalid_json
@check_token
@game_chequed
def add_game_to_order(request, order, game):
    
    order.games.add(game)

    games_count = order.games.count()
    print(
        f'Order ID: {order.pk}, User: {order.user}, Game Slug: {game.slug}, Games Count: {games_count}'
    )

    return JsonResponse({'num-games-in-order': games_count}, status=200)


@csrf_exempt
@post_required
@order_status
@check_token
@owner_order
def change_order_status(request, order,status):
    if status not in [Order.Status.CONFIRMED, Order.Status.CANCELLED,Order.Status.PAID]:
        return JsonResponse({'error': 'Invalid status'}, status=400)

    if order.status != Order.Status.INITIATED and status in [Order.Status.CONFIRMED, Order.Status.CANCELLED]:
        print('ORDER STATUS:',order.status,' STATUS:',status)
        return JsonResponse(
            {'error': 'Orders can only be confirmed/cancelled when initiated'}, status=400
        )
    if order.status == Order.Status.INITIATED and status == Order.Status.PAID:
        return JsonResponse( {'error': 'Invalid status'}, status=400)

    order.status = status
    order.save()

    if status == Order.Status.CANCELLED:
        for game in order.games.all():
            game.stock += 1
            game.save()
    print(JsonResponse(
        {'status': order.get_status_display()}, status=200
    ))
    return JsonResponse(
        {'status': order.get_status_display()}, status=200
    )




@post_required
@check_token
@owner_order
@check_card
def pay_order(request, order):
    if order.status != Order.Status.CONFIRMED:
        return JsonResponse({'error': 'Orders can only be paid when confirmed'}, status=400)
    
    order.status = Order.Status.PAID
    order.save()
    return JsonResponse({'status': 'Paid'})



