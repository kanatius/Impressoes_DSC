from django.shortcuts import render

# Create your views here.
def homePage(request):
    return render(request, 'home.html', {'usuario' : 'Natan Almeida'})

def comoFunciona(request):
    return render(request, "comofunciona.html")