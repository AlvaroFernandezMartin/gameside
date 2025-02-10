from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import get_required, post_required

from .decorators import check_token
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
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)

    if request.user != order.user:
        return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)

    serializer = OrderSerializer(order, request=request)
    return serializer.json_response()


@csrf_exempt
@get_required
@check_token
def order_game_list(request, pk):
    pass
