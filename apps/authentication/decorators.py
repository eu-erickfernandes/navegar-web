from django.urls import reverse
from django.shortcuts import redirect

def redirect_authenticated_user(view):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('route:index'))
        
        return view(request)
    
    return wrapper