from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('account/', views.profile, name='account'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('add-address/', views.add_address, name='add_address'),
    path('account/edit-address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    # path('password_reset/done/', views.password_reset_done_view, name='password_reset_done'),
    # path('password_reset_confirm/<uidb64>/<token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    # path('password_reset_complete/', views.password_reset_complete_view, name='password_reset_complete'),
    # path('verify/<str:token>/', views.verify_magic_link, name='verify_magic_link'),
    # path('profile/', views.profile_view, name='profile'),
    # path('checkout/', views.checkout_view, name='checkout'),
    # path('order_history/', views.order_history_view, name='order_history'),
    # path('wishlist/', views.wishlist_view, name='wishlist'),
    # path('account/coupons/', views.coupons_view, name='coupons'),
    # path('account/addresses/', views.addresses_view, name='addresses'),
    # path('account/orders/', views.orders_view, name='orders'),
    # path('account/reviews/', views.reviews_view, name='reviews'),
    # path('account/settings/', views.settings_view, name='settings'),
] 