from django.db import models
from django.utils import timezone
from django.db.models.signals import post_delete
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin,AbstractUser
from shop.models import Product,ProductCat,ProductImage
from django.conf import settings
from django.dispatch import receiver
import os,random,uuid

class CustomeUserManager(BaseUserManager):
    def create_user(self,username,name,password=None,**extra_fields):
        if not username:
            raise ValueError("Users must have an email address")
        username = self.normalize_email(username)

        user = self.model(username=username,name=name,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,name,password=None,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_active",True)
        return self.create_user(username,name,password,**extra_fields)


class CustomUser(AbstractUser):
    username = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomeUserManager()
    # Magic link fields

    magic_link_token = models.UUIDField(default=uuid.uuid4, editable=False)
    magic_link_expiration = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']  

    def __str__(self):
        return self.username
    
# class ProductReview(models.Model):
#     product = models.ForeignKey(Product,on_delete=models.CASCADE)
#     user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
#     review = models.TextField()
#     rating = models.PositiveIntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.user.name} - {self.product.sku}"
    
class Order(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.name}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.order.user.name} - {self.product.sku}"
    
class Cart(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name if self.user else 'Guest'} - {self.product.sku}"

    def get_total_price(self):
        return self.quantity * (self.product.discounted_price if self.product.is_discounted else self.product.price)

class Coupon(models.Model):
    code = models.CharField(max_length=255)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
        
class Address(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name} - {self.address}"         
    
class Payment(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.order.user.name} - {self.amount}"
    
class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name} - {self.product.sku}"
    
