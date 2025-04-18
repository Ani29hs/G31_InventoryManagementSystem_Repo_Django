from django.contrib import admin

from .models import Product, WarehouseAddress, Warehouse, User

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'price', 'quantity', 'category', 'warehouse', 'user')
    search_fields = ('name',)
    list_filter = ('category', 'warehouse')

admin.site.register(Product, ProductAdmin)

class WarehouseAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'address')
    search_fields = ('address',)

admin.site.register(WarehouseAddress, WarehouseAddressAdmin)

class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('Warehouse_id', 'product_id', 'from_warehouse', 'to_warehouse', 'quantity_to_transfer', 'transfer_date', 'status')
    search_fields = ('from_warehouse__address', 'to_warehouse__address')
    list_filter = ('status',)

admin.site.register(Warehouse, WarehouseAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('is_staff',)

admin.site.register(User, UserAdmin)

