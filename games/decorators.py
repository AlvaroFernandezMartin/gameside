from django.http import HttpResponseNotAllowed


def get_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.method != 'GET':
            return HttpResponseNotAllowed(['GET'])
        return view_func(request, *args, **kwargs)

    return wrapped_view
