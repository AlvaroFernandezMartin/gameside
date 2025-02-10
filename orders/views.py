import re
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import post_required
from users.models import Token

from .models import Order
from .OrderSerializer import OrderSerializer


@csrf_exempt
@post_required
def add_order(request):
    token_header = request.headers.get('Authorization')
    
    if not token_header:
        return JsonResponse({'error': 'Authorization token is missing'}, status=403)

    match = re.fullmatch(
        r'Bearer (?P<token_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12})',
        token_header
    )

    if not match:
        return JsonResponse({'error': 'Invalid authentication token format'}, status=400)

    token_str = match.group('token_id') 
    try:
        token_obj = Token.objects.get(key=token_str)
    except Token.DoesNotExist:
        return JsonResponse({'error': 'Unregistered authentication token'}, status=401)

    
    user = token_obj.user  

    
    order = Order.objects.create(
        status=1,
        user=user,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    return JsonResponse({'id': order.pk}, status=200)


  






def order_detail(request, pk):
    order = Order.objects.filter(pk=pk)
    if not order.exists():
        return JsonResponse({'error': 'No order found'}, status=404)

    serializer = OrderSerializer(order, request=request)
    return serializer.json_response()
