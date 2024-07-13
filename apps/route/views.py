from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'route/index.html')

@login_required
def boats(request):
    return render(request, 'route/boats.html')

@login_required
def search(request):
    return render(request, 'route/search.html')
