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
    order = Order.objects.create(
        status=1,
        user=request.user,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    return JsonResponse({'id': order.pk}, status=200)


@csrf_exempt
@get_required
@check_token
@owner_order
def order_detail(request, pk):
    order = Order.objects.get(pk=pk)

    serializer = OrderSerializer(order, request=request)
    return serializer.json_response()


@csrf_exempt
@get_required
@check_token
@owner_order
def order_game_list(request, pk):
    order = Order.objects.get(pk=pk)

    games = order.games.all()

    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


@csrf_exempt
@post_required
@check_token
@owner_order
def add_game_to_order(request, pk):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    slug = body.get('game-slug')
    if not slug:
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    try:
        game = Game.objects.get(slug=slug)
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)

    order = Order.objects.get(pk=pk)

    if order.user != request.user:
        return JsonResponse({'error': 'Forbidden: You are not the owner of this order'}, status=403)

    order.games.add(game)

    games_count = order.games.count()

    print(
        f'Order ID: {order.pk}, User: {order.user}, Game Slug: {game.slug}, Games Count: {games_count}'
    )

    return JsonResponse({'num-games-in-order': games_count}, status=200)
