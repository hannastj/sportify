from django.contrib import admin
from django.urls import path, include
from sportify_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', include('sportify_app.urls')),
    path('admin/', admin.site.urls),
    path('', include('sportify_app.urls')),
]
