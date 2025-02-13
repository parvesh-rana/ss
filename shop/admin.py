from django.contrib import admin
from .models import ProductCat,ProductImage,HomepageBanner,Product
# Register your models here.


# Custom Admin for ProductImage to be inline within Product admin
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ( 'sku', 'is_primary', 'image')
    list_filter = ['sku']  # Add filters for product and variant
    search_fields = ['sku',] # Add search functionality
    list_editable = ['is_primary',]  # Make 'is_primary' editable in the list view
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ('productcat','sku','flavour','size','size_unit','price','is_discounted','discounted_price','stock','bestselling_rank','created_at','updated_at')
    list_filter = ('sku','size','is_discounted')
    ordering = ['bestselling_rank']
    fieldsets = (
        (None, {
            'fields': ('productcat','sku','flavour','size','front_image','size_unit','price','is_discounted','discounted_price','stock','bestselling_rank')
        }),)
    def save_model(self, request, obj, form, change):
        if obj.is_discounted and not obj.discounted_price:
            raise ValidationError("Discounted price is required during the discount period.")
        super().save_model(request, obj, form, change)

class ProductCatAdmin(admin.ModelAdmin):
    # Fields to display in the list view (the table)
    list_display = ('product_type','name', 'brand','created_at', 'updated_at','is_active')
    
    # Fields to allow search functionality
    search_fields = ('name', 'brand')
    
    # Ordering the list view by creation date (most recent first)
    ordering = ('-created_at',)
    
    # Customize form fields for product creation/editing (optional)
    fieldsets = (
        (None, {
            'fields': ('product_type','name', 'brand', 'description','is_active')
        }),
        
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    # Make discounted_price required only if is_discounted is True (validation logic)
    

class HomepageBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'display_order', 'updated_at')
    list_editable = ('is_active', 'display_order')
    search_fields = ('title',)
    list_filter = ('is_active',)


admin.site.register(HomepageBanner, HomepageBannerAdmin)
admin.site.register(ProductCat,ProductCatAdmin)
admin.site.register(ProductImage,ProductImageAdmin)
admin.site.register(Product,ProductAdmin)

