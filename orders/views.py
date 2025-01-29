from django.http import JsonResponse

from .models import Order
from .OrderSerializer import OrderSerializer

# Create your views here.


def add_order(request):
    pass


def order_detail(request, pk):
    order = Order.objects.filter(pk=pk)
    if not order.exists():
        return JsonResponse({'error': 'No games found'}, status=404)

    serializer = OrderSerializer(order, request=request)
    return serializer.json_response()
