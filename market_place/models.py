from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# Custom User Model
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

# Profile Model
class Profile(models.Model):
    USER_TYPES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)

    def __str__(self):
        return self.user.email
    
import uuid
from django.utils.deconstruct import deconstructible
from django.core.files.storage import default_storage

@deconstructible
class UniqueImageName(object):
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{ext}"
        return f"item_images/{unique_filename}"


class Item(models.Model):
    CATEGORY_CHOICES = [
        ('equipment', 'Equipment'),
        ('crop', 'Crop'),
        ('fertilizer', 'Fertilizer'),
        ('pesticides', 'Pesticides'),
        ('other', 'Other'),
    ]

    seller = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='item_images/', null=True, blank=True)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.name


# Cart Model
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through='CartItem')

    def __str__(self):
        return f"{self.user.email}'s Cart"

# CartItem Model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

# Order Model
class Order(models.Model):
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField(Item)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.buyer.user.email}"
