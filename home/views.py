from django.shortcuts import render

# Create your views here.

def index(request):
    """
    Renders index template
    """
    return render(request, 'home/index.html')