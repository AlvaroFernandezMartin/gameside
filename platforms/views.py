from shared.decorators import get_required
from django.http import JsonResponse
from .models import Platform
from .PlatformSerializers import PlatformSerializer


@get_required
def platform_list(request):
    all_platforms = Platform.objects.all()

    serializer = PlatformSerializer(all_platforms, request=request)
    return serializer.json_response()


@get_required
def platform_detail(request, slug):

    
    platforms_detail = Platform.objects.filter(slug=slug)

    if not platforms_detail.exists():
        return JsonResponse({'error': 'No platforms found'}, status=404)
    
    serializer = PlatformSerializer(platforms_detail, request=request)
    return serializer.json_response()
