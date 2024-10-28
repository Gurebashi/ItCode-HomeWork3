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
from django.urls import path, include
from shop.views import display_image
from django.contrib.auth import views as auth_views
from shop import views
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
router=DefaultRouter()

router.register('painters',views.PainterAPI,basename='painters')
router.register('pictures',views.PictureAPI,basename='pictures')
urlpatterns = [
    path("admin/", admin.site.urls),
    path('add_to_cart/<int:pk>/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('remove_from_cart/<int:pk>/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('picture_list/', views.PictureListView.as_view(), name='pictures_list'),
    path("media/<str:image_name>", display_image, name="display_image"),
    path('picture/<int:pk>/delete', views.PictureDeleteView.as_view(), name='pictures_delete'),
    path('picture/<int:pk>/update/', views.PictureUpdateView.as_view(), name='pictures_update'),
    path('picture/<int:pk>/', views.PictureDetailView.as_view(), name='pictures_detail'),
    path('picture/create', views.PictureCreateView.as_view(), name='pictures_create'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/',views.MyLoginView.as_view(), name='login'),
    path('register/',views.RegisterView.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/profile/', views.profile_view, name='profile'),
]+router.urls
