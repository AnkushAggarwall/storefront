from django.shortcuts import render
from django.http import HttpResponse
from  django.db.models.aggregates import Count, Min, Max, Avg
from store.models import Product

def say_hello(request):
    result = Product.objects.aggregate(count=Count('id'), min_price=Min('unit_price'), max_price=Max('unit_price'), avg_price=Avg('unit_price'))
    return render(request, 'hello.html', {'name': 'Mosh', 'result': result})
