from django.http import JsonResponse

from shared.decorators import get_required
from django.views.decorators.csrf import csrf_exempt

from .CategoriesSerializer import CategorieSerializer
from .models import Category

@csrf_exempt
@get_required
def categorie_list(request):
    all_categories = Category.objects.all()
    serializer = CategorieSerializer(all_categories, request=request)
    return serializer.json_response()

@csrf_exempt
@get_required
def categorie_detail(request, slug):
    categories_detail = Category.objects.filter(slug=slug)

    if not categories_detail.exists():
        return JsonResponse({'error': 'No categories found'}, status=404)

    serializer = CategorieSerializer(categories_detail, request=request)
    return serializer.json_response()
