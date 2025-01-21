from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="home" ),
    path("product/<str:product_name>/", views.product_detail, name="product_detail" ),
]