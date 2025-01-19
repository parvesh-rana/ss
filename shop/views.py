from django.shortcuts import render
from .models import ProductCat,Product,ProductImage,HomepageBanner
from django.http import HttpResponse

# Create your views here.
def index(request):
    banners=HomepageBanner.objects.all()
    print(banners)
    best=Product.objects.order_by('bestselling_rank')[:4]
    print(best)
    return render(request, 'homepage.html',{
        'banners':banners,
        'best':best,
    })
   