from django.http import JsonResponse

from shared.decorators import get_required
from django.views.decorators.csrf import csrf_exempt

from .CategoriesSerializer import CategorieSerializer
from .models import Category


@get_required
def categorie_list(request):
    all_categories = Category.objects.all()
    serializer = CategorieSerializer(all_categories, request=request)
    return serializer.json_response()

@get_required
def categorie_detail(request, slug):
    try:
        categories_detail = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)
    
    serializer = CategorieSerializer(categories_detail, request=request)
    return serializer.json_response()