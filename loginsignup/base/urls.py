from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from base import views
from base.views import register, index, custom_login, product_detail,medicine_detail

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", index, name="index"),
    path("signup/", register, name="register"),
    path("login/", custom_login, name="custom_login"),
    path("admin/", admin.site.urls),
    path('about', views.about, name="about"),
    path('home', views.home, name="home"),
    path('product/', views.product, name="product"),
    path("medicines", views.medicines, name="medicines"),
    path("products/<int:product_id>", product_detail, name="product_detail"),
    path("medicines/<int:product_id>", medicine_detail, name="medicine_detail"),  # Correct URL pattern with product ID capture
    path('logout', views.HandleLogout, name="HandleLogout"),
    path("orders",views.myorders,name="myorders"),
    path('user_details/', views.user_details, name='user_details'),
    path("search",views.search,name="search"),
    path("ayurveda", views.ayurveda, name="ayurveda"),
    # path("medicines/<int:medicine_id>", med_detail, name="med_detail"),
    path("blogs",views.blog_category_view, name='blog_category_view'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('videos/', views.video_list, name='video_list'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)