from django.http import JsonResponse

from .decorators import get_required
from .models import Game, Review
from .Serializers.GameSerializer import GameSerializer, ReviewSerializer


@get_required
def game_list(request):
    all_games = Game.objects.all()

    serializer = GameSerializer(to_serialize=all_games, request=request)
    serialized_data = serializer.serialize()

    return JsonResponse(serialized_data, safe=False)


@get_required
def game_detail(request, slug):
    games_detail = Game.objects.filter(slug=slug)

    if not games_detail.exists():
        return JsonResponse({'error': 'No games found'}, status=404)

    serializer = GameSerializer(to_serialize=games_detail, request=request)
    serialized_data = serializer.serialize()

    return JsonResponse(serialized_data, safe=False)


@get_required
def review_list(request):
    all_reviews = Review.objects.all()

    serializer = ReviewSerializer(to_serialize=all_reviews, request=request)
    serialized_data = serializer.serialize()

    return JsonResponse(serialized_data, safe=False)


@get_required
def review_detail(request, pk):
    reviews_detail = Review.objects.filter(pk=pk)

    if not reviews_detail.exists():
        return JsonResponse({'error': 'No games found'}, status=404)

    serializer = ReviewSerializer(to_serialize=reviews_detail, request=request)
    serialized_data = serializer.serialize()

    return JsonResponse(serialized_data, safe=False)
