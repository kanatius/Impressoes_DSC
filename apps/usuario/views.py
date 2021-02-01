from django.shortcuts import render, redirect
from .models import Usuario

#usuario

# Create your views here.
def login(request):
    if request.method == "POST":
        return render(request, "login_efetuado.html")
    else:
        return redirect("/")