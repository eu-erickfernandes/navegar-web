from django.urls import reverse
from django.shortcuts import redirect
from django.http import Http404

def redirect_authenticated_user(view):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('route:search'))
        
        return view(request)
    
    return wrapper


def required_user_roles(*roles):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if request.user.role in roles:
                return view(request, *args, **kwargs)
            
            raise Http404
            
        return wrapper
    
    return decorator