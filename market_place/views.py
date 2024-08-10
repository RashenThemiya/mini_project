from django.shortcuts import render

def index(request):
    return render(request, 'market_place.html')
