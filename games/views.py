from django.http import JsonResponse

from shared.decorators import get_required

from .models import Game, Review
from .Serializers.GameSerializer import GameSerializer, ReviewSerializer


@get_required
def game_list(request):
    all_games = Game.objects.all()

    serializer = GameSerializer(all_games, request=request)
    return serializer.json_response()


@get_required
def game_detail(request, slug):
    games_detail = Game.objects.filter(slug=slug)

    if not games_detail.exists():
        return JsonResponse({'error': 'No games found'}, status=404)

    serializer = GameSerializer(games_detail, request=request)
    return serializer.json_response()


@get_required
def review_list(request, slug):
    all_reviews = Review.objects.all()

    serializer = ReviewSerializer(all_reviews, request=request)

    return serializer.json_response()


@get_required
def review_detail(request, pk):
    reviews_detail = Review.objects.filter(pk=pk)

    if not reviews_detail.exists():
        return JsonResponse({'error': 'No games found'}, status=404)

    serializer = ReviewSerializer(reviews_detail, request=request)
    return serializer.json_response()
