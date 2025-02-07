from django.http import JsonResponse


def get_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.method != 'GET':
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        return view_func(request, *args, **kwargs)

    return wrapped_view


def post_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.method != 'POST':
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        return view_func(request, *args, **kwargs)

    return wrapped_view
