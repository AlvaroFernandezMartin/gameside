import json
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import get_required
from users.models import Token

from .models import Game, Review
from .Serializers.GameSerializer import GameSerializer, ReviewSerializer

@csrf_exempt
@get_required
def game_list(request):
    all_games = Game.objects.all()

    serializer = GameSerializer(all_games, request=request)
    return serializer.json_response()

@csrf_exempt
@get_required
def game_detail(request, slug):
    games_detail = Game.objects.filter(slug=slug)

    if not games_detail.exists():
        return JsonResponse({'error': 'No games found'}, status=404)

    serializer = GameSerializer(games_detail, request=request)
    return serializer.json_response()

@csrf_exempt
@get_required
def review_list(request, slug):
    all_reviews = Review.objects.all()

    serializer = ReviewSerializer(all_reviews, request=request)

    return serializer.json_response()

@csrf_exempt
@get_required
def review_detail(request, pk):
    reviews_detail = Review.objects.filter(pk=pk)

    if not reviews_detail.exists():
        return JsonResponse({'error': 'No games found'}, status=404)

    serializer = ReviewSerializer(reviews_detail, request=request)
    return serializer.json_response()


@csrf_exempt
def add_review(request, slug):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        # Cargar el cuerpo de la solicitud como JSON
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    # Verificar si el campo 'token' está presente en el cuerpo de la solicitud
    if 'token' not in body:
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    # Intentar obtener y verificar el token
    token_str = body['token']
    try:
        user = Token.objects.get(token=token_str)
    except:
        return JsonResponse({'error': 'Invalid token'}, status=401)

    # Verificar que los campos de rating y comment estén presentes
    if 'rating' not in body or 'comment' not in body:
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    rating = body['rating']
    if not (0 <= rating <= 5):
        return JsonResponse({'error': 'Rating is out of range'}, status=400)

    try:
        game = Game.objects.get(slug=slug)
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)

    review = Review.objects.create(
        game=game,
        author=user,
        rating=rating,
        comment=body['comment'],
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    return JsonResponse(
        {'id': review.pk, 'rating': review.rating, 'comment': review.comment}, status=200
    )
