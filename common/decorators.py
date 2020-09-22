from django.http import HttpResponseBadRequest
# custom ajax_required decorator wch wraps a function that returns an HttpResponseBadRequest object  otherwise it returns the decorated function

def ajax_required(f):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)

    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap