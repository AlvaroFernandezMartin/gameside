import re

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import post_required
from users.models import Token

from .models import Order
from .OrderSerializer import OrderSerializer


@csrf_exempt
@post_required
def add_order(request):
    token = request.headers.get('Authorization')

    m = re.fullmatch(
        r'Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12})',
        token,
    )

    if not m:
        return JsonResponse({'error': 'Invalid authentication token'}, status=400)
    try:
        token_obj = Token.objects.get(key=m['token'])
    except Token.DoesNotExist:
        return JsonResponse({'error': 'Unregistered authentication token'}, status=401)

    user = request.user = token_obj.user


def order_detail(request, pk):
    order = Order.objects.filter(pk=pk)
    if not order.exists():
        return JsonResponse({'error': 'No games found'}, status=404)

    serializer = OrderSerializer(order, request=request)
    return serializer.json_response()
