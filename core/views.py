from django.shortcuts import render

# Create your views here.
def homePage(request):
    return render(request, 'home.html')

def comoFunciona(request):
    return render(request, "comofunciona.html")