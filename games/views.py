import json
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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

    serializer = GameSerializer(all_games, many=True)

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
    all_reviews = Review.objects.all()

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
def add_review(request, slug):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    token = request.headers['Token']
    
   
    try:
        user = Token.objects.get(key=token).user
    except :
        return JsonResponse({'error': 'Invalid token'}, status=401)

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
