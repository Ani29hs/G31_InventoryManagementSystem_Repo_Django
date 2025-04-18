from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models
from django.conf import settings 

class User(AbstractUser):
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(max_length=50, default='user')
    
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    USERNAME_FIELD = "email"  
    REQUIRED_FIELDS = ["username"]  

    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

    def __str__(self):
        return self.email
    

    

class WarehouseAddress(models.Model):
    id=models.AutoField(primary_key=True)
    address=models.CharField(max_length=255)


    def __str__(self):
        return self.address
    


class Product(models.Model):
    product_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    price=models.IntegerField()
    quantity=models.IntegerField()

    CATEGORY_CHOICES = (
        ('Electronics', 'Electronics'),
        ('Stationary', 'Stationary'),
        ('HomeAppliances', 'HomeAppliances'),
    )

    

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    warehouse = models.ForeignKey(WarehouseAddress, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')



    def __str__(self):
        return self.name
    
class Warehouse(models.Model):
    Warehouse_id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='warehouses')
    from_warehouse=models.ForeignKey(WarehouseAddress, on_delete=models.CASCADE, related_name='from_warehouse')
    to_warehouse=models.ForeignKey(WarehouseAddress, on_delete=models.CASCADE, related_name='to_warehouse')
    quantity_to_transfer=models.IntegerField()
    transfer_date=models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transfers') 

    STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Transferred', 'Transferred')
]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Transfer from {self.from_warehouse} to {self.to_warehouse}"

