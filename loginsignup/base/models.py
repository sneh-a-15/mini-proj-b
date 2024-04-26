from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser,BaseUserManager
# from django.contrib.auth.models import User
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# Create your models here.
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    birth_date = models.DateField(default=timezone.now)
    gender = models.CharField(max_length=10,default='')
     # You should use a more secure way to store passwords

    objects = CustomUserManager()
    def __str__(self):
        return self.email
    
class Medicines(models.Model):
    medicine_name=models.CharField(max_length=250)
    medicine_image=models.ImageField(upload_to="products",blank=True,null=True)
    medicine_price=models.IntegerField()
    medicine_descripton=models.TextField()
    medicine_exp=models.DateField()
    def __str__(self):
        return self.medicine_name


class ProductItems(models.Model):
    prod_name=models.CharField(max_length=250)
    prod_image=models.ImageField(upload_to="products",blank=True,null=True)
    prod_price=models.IntegerField()
    prod_descripton=models.TextField()
    prod_exp=models.DateField(default=timezone.now)
    
    def __str__(self):
        return self.prod_name

class MyOrders(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField()
    items=models.CharField(max_length=1500)
    address=models.TextField()
    quantity=models.CharField(max_length=100)
    price=models.CharField(max_length=100)
    phone_num=models.CharField(max_length=10)
    delivery=models.BooleanField(default=False)
    pending=models.BooleanField(default=False)
   
    def __int__(self):
        return self.id

class Review(models.Model):
    product = models.ForeignKey(ProductItems, on_delete=models.CASCADE, related_name='reviews')  # Update 'Product' to 'ProductItems'
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=((1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')))
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.prod_name} - {self.rating}"
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment'] 

class Ayurveda(models.Model):
    med_name=models.CharField(max_length=250)
    med_image=models.ImageField(upload_to="products",blank=True,null=True)
    med_price=models.IntegerField()
    med_descripton=models.TextField()
    med_exp=models.DateField()
    def __str__(self):
        return self.med_name