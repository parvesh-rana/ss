from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from datetime import datetime,timedelta
from .models import ProductCat,Product,ProductImage,HomepageBanner
from django.http import HttpResponse

# Create your views here.
def index(request):
    banners=HomepageBanner.objects.all()
    best=Product.objects.order_by('bestselling_rank')[:4]
    return render(request, 'homepage.html',{
        'banners':banners,
        'best':best,
    })
def product_detail(request,product_name):
    product = get_object_or_404(Product, sku=product_name)
    print(product)
    images = ProductImage.objects.filter(sku=product)
    return render(request, 'product.html',{'product':product,'images':images})
   