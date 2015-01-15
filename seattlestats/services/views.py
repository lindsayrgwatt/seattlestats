from django.shortcuts import render_to_response
from services.models import Police911Response

def home(request):
    total = Police911Response.objects.count()
    earliest = Police911Response.objects.earliest('date')
    latest = Police911Response.objects.latest('date')
    
    context = {
        'total':total,
        'earliest':earliest.date,
        'latest':latest.date,
    }
    
    return render_to_response('home.html', context)
