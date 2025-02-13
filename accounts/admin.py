from django.contrib import admin
from .models import CustomUser,Address,Payment,Wishlist,Coupon,Order,OrderItem,Cart
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email','name','is_active','is_staff','is_superuser','last_login','date_joined')
    list_filter = ('is_active','is_staff','is_superuser')
    search_fields = ('email','name')
    ordering = ('-date_joined',)



admin.site.register(CustomUser,CustomUserAdmin)






