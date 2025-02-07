import json

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import post_required


@csrf_exempt
@post_required
def auth(request):
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    if 'username' not in payload or 'password' not in payload:
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    if user := authenticate(username=payload['username'], password=payload['password']):
        return JsonResponse({'token': user.token.key})

    return JsonResponse({'error': 'Invalid credentials'}, status=401)
