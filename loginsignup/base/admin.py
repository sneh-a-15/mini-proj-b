from django.contrib import admin

# Register your models here.
from .models import CustomUser,Medicines,ProductItems,Review,MyOrders,Ayurveda,BlogPost,Video

admin.site.register(CustomUser)
admin.site.register(Medicines)
admin.site.register(ProductItems)
admin.site.register(Review)
admin.site.register(MyOrders)
admin.site.register(Ayurveda)
admin.site.register(BlogPost)
admin.site.register(Video)