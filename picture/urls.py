"""
URL configuration for picture project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from shop.views import display_image
from shop import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('picture_list/', views.PictureListView.as_view(), name='pictures_list'),
    path("media/<str:image_name>", display_image, name="display_image"),
    path('picture/<int:pk>/delete', views.PictureDeleteView.as_view(), name='pictures_delete'),
    path('picture/<int:pk>/update/', views.PictureUpdateView.as_view(), name='pictures_update'),
    path('picture/<int:pk>/', views.PictureDetailView.as_view(), name='pictures_detail'),
    path('picture/create', views.PictureCreateView.as_view(), name='pictures_create'),
]
