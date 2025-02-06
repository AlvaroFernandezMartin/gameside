import json
import re
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from shared.decorators import get_required
from users.models import Token

from .models import Game, Review
from .Serializers.GameSerializer import GameSerializer, ReviewSerializer


@get_required
def game_list(request):
    all_games = Game.objects.all()

    category = request.GET.get('category')
    platform = request.GET.get('platform')

    if category:
        all_games = all_games.filter(category__slug=category)

    if platform:
        all_games = all_games.filter(platforms__slug=platform)

    serializer = GameSerializer(all_games, request=request)

    return serializer.json_response()


@get_required
def game_detail(request, slug):
    try:
        games_detail = Game.objects.get(slug=slug)
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)

    serializer = GameSerializer(games_detail, request=request)
    return serializer.json_response()


@get_required
def review_list(request, slug):
    try:
        game = Game.objects.get(slug=slug)
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)

    all_reviews = game.reviews.all()
    serializer = ReviewSerializer(all_reviews, request=request)

    return serializer.json_response()


@get_required
def review_detail(request, pk):
    try:
        reviews_detail = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return JsonResponse({'error': 'Review not found'}, status=404)

    serializer = ReviewSerializer(reviews_detail, request=request)
    return serializer.json_response()


@csrf_exempt
@require_POST
def add_review(request, slug):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    token = request.headers.get('Authorization')

    if not token:
        return JsonResponse({'error': 'Authorization token is missing'}, status=403)
    m = re.fullmatch(
        r'Bearer (?P<token_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12})',
        token,
    )

    if not m:
        return JsonResponse({'error': 'Invalid authentication token'}, status=400)
    try:
        token_obj = Token.objects.get(key=m['token'])
    except Token.DoesNotExist:
        return JsonResponse({'error': 'Unregistered authentication token'}, status=401)

    user = request.user = token_obj.user
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
