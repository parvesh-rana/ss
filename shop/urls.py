from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name="shop"

urlpatterns = [
    path("", views.index, name="home" ),
    path("product/<str:product_name>/", views.product_detail, name="product_detail" ),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('stores/', TemplateView.as_view(template_name='stores.html'), name='stores'),
    path('terms/', TemplateView.as_view(template_name='terms.html'), name='terms'),
    path('privacy-policy/', TemplateView.as_view(template_name='privacy.html'), name='privacy'),
]