from django.db import models
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError

class ProductCat(models.Model):
    PRODUCT_TYPE_CHOICES=[
        ('Whey Protein', 'Whey Protein'),
        ('Mass Gainer', 'Mass Gainer'),
        ('Pre Workout', 'Pre Workout'),
        ('Peanut Butter', 'Peanut Butter'),
        ('Protein Bar', 'Protein Bar'),
    ]
    
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    product_type = models.CharField(
        max_length=100,
        choices=PRODUCT_TYPE_CHOICES,
        )
    
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    productcat = models.ForeignKey(ProductCat, on_delete=models.CASCADE, related_name="productcat")
    sku = models.CharField(max_length=100, unique=True)
    flavour = models.CharField(max_length=255)  # e.g., "Chocolate", "Honey"
    size = models.PositiveIntegerField()
    SIZE_UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('gm', 'Gram'),
    ]
    size_unit = models.CharField(
        max_length=2, 
        choices=SIZE_UNIT_CHOICES, 
        default='kg'  # Default to kg
        )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    front_image = models.ImageField(upload_to='front_images/')
    is_discounted = models.BooleanField(default=False)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Discounted price (can be null)
    bestselling_rank = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()  # Stock count
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_discount_percentage(self):
        if self.discounted_price and self.price:
            return int(round(((self.price - self.discounted_price) / self.price) * 100, 2))
        return 0
    def __str__(self):
        return f"{self.sku}"


class ProductImage(models.Model):
# Image related to the product
    sku = models.ForeignKey(Product,on_delete=models.CASCADE,to_field="sku",related_name="images")
    image = models.ImageField(upload_to='product_images/')
    is_primary = models.BooleanField(default=False)
    alt_text = models.CharField(max_length=255, blank=True, null=True)  # Optional alt text
    image_order = models.PositiveIntegerField(default=0)  # Optional field for ordering images
    
    def __str__(self):
        return f"Image -{self.image_order}- {self.sku} - {self.alt_text}"
@receiver(post_delete, sender=ProductImage)
def delete_image_file(sender, instance, **kwargs):
    if instance.image:
        image_path = instance.image.path
        if os.path.isfile(image_path):
            os.remove(image_path)

class HomepageBanner(models.Model):
    title = models.CharField(max_length=100)  # For identifying the image
    image = models.ImageField(upload_to='homepage_banners/')  # Folder for these images
    # link_url = models.URLField(blank=True, null=True)  # Optional link for redirection
    is_active = models.BooleanField(default=True)  # To toggle visibility
    display_order = models.PositiveIntegerField(default=0)  # For ordering banners
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order']  # Default ordering

    def __str__(self):
        return self.title