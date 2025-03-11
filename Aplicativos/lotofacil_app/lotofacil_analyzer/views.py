from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  # Crie um template 'home.html' depois

