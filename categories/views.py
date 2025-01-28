from shared.decorators import get_required

from .CategoriesSerializer import CategorieSerializer
from .models import Category


@get_required
def categorie_list(request):
    all_categories = Category.objects.all()
    serializer = CategorieSerializer(all_categories, request=request)
    return serializer.json_response()


@get_required
def categorie_detail(request, slug):
    categories_detail = Category.objects.filter(slug=slug)
    serializer = CategorieSerializer(categories_detail, request=request)
    return serializer.json_response()
