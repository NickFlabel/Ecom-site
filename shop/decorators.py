from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.response import Response

def unauthenticated_user(func):
    """This decorator does not allow authenticated user to access the decorated
    view
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('ecom:store')
        else:
            return func(request, *args, **kwargs)

    return wrapper

def allowed_users(allowed_roles=[]):
    def decorator(func):
        def wrapper(request, *args, **kwargs):

            groups = None

            if request.user.groups.exists():
                groups = request.user.groups.all()

            if groups:
                for group in groups:
                    if group.name in allowed_roles:
                        return func(request, *args, **kwargs)
                else:
                    return HttpResponse('You are not authorized to view that page')

        return wrapper
    return decorator


def the_same_user(func):
    def wrapper(request, pk, *args, **kwargs):
        if request.user.id == pk:
            return func(request, pk, *args, **kwargs)
        else:
            content = {
            'status': 'request was denied'
            }
            return Response(content)

    return wrapper

