from django.contrib import admin

# Register your models here.
from .models import CustomUser,Medicines,ProductItems,Review,MyOrders,Ayurveda,BlogPost, Symptoms_medicine,Video,Skincare,Prescription

admin.site.register(CustomUser)
admin.site.register(Medicines)
admin.site.register(ProductItems)
admin.site.register(Review)
admin.site.register(MyOrders)
admin.site.register(Ayurveda)
admin.site.register(BlogPost)
admin.site.register(Video)
admin.site.register(Skincare)
admin.site.register(Prescription)
admin.site.register(Symptoms_medicine)