from django.db import models
from django.forms import ValidationError

# class Category(models.Model):
    # name = models.CharField(max_length=100, unique=True)

    # def __str__(self):
    #     return self.name

class Admin(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField()
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.name

from django.db import models

# ------------------ USER ------------------
class Register(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField()
    number = models.CharField(max_length=12)
    address = models.TextField()
    password = models.CharField(max_length=128)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    status = models.CharField(max_length=20, default="active")  # active / blocked

    def __str__(self):
        return self.name


class Renter(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField()
    number = models.CharField(max_length=12)
    rental_business_name = models.CharField(max_length=100)
    rental_address = models.TextField()

    gst_number = models.CharField(max_length=15, null=True, blank=True)
    license_number = models.CharField(max_length=50, null=True, blank=True)

    password = models.CharField(max_length=128)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Seller(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField()
    number = models.CharField(max_length=12)
    shop_name = models.CharField(max_length=100)
    shop_address = models.TextField()

    gst_number = models.CharField(max_length=15, null=True, blank=True)
    license_number = models.CharField(max_length=50, null=True, blank=True)

    password = models.CharField(max_length=128)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Furniture(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('rent', 'Rent'),
        ('sale', 'Sale'),
    ]

    seller = models.ForeignKey('Seller', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # ✅ Link with Category
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to="product_image")
    description = models.TextField()
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE_CHOICES)

    def __str__(self):
        return f"{self.product_name} ({self.get_product_type_display()})"


class RentalFurniture(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # ✅ Link with Category
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    availability = models.BooleanField(default=True)
    image = models.ImageField(upload_to="rental_furniture")
    owner = models.ForeignKey('Renter', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {'Available' if self.availability else 'Not Available'}"



class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]

    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    furniture_product = models.ForeignKey(Furniture, null=True, blank=True, on_delete=models.CASCADE)
    rental_product = models.ForeignKey(RentalFurniture, null=True, blank=True, on_delete=models.CASCADE)
    buyer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    delivery_location = models.TextField()
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')  #
    is_approved=models.BooleanField(default=False)

    def clean(self):
        if self.furniture_product and self.rental_product:
            raise ValidationError("An order cannot have both furniture and rental products.")
        if not self.furniture_product and not self.rental_product:
            raise ValidationError("An order must have either a furniture or rental product.")

class Product(models.Model):
    PRODUCT_TYPES = [
        ('rent', 'For Rent'),
        ('sale', 'For Sale'),
    ]

    name = models.CharField(max_length=255)
    stock = models.IntegerField(default=0)  # Added default value for stock
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPES, default='sale')
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    seller = models.ForeignKey(Register, on_delete=models.CASCADE, related_name="seller_products", blank=True, null=True)
    renter = models.ForeignKey(Register, on_delete=models.CASCADE, related_name="renter_products", blank=True, null=True)

    def _str_(self):
        return self.name



class Booking(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Register, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')
from django.db import models
from django.contrib.auth.models import User  # Ensure you're using the correct User model


class Shop(models.Model):
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.name



# models.py
from django.db import models

class Notification(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    message = models.TextField()
    status = models.CharField(max_length=10)  # e.g., "Approved", "Rejected"
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.user.name}"


