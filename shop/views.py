from lib2to3.fixes.fix_input import context

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, JsonResponse
from PIL import Image
from django.conf import settings
import os
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView, ListView
from django_filters.views import FilterView
from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate
from shop import filters
from shop.forms import UserRegisterForm
from shop.models import Picture
from rest_framework import viewsets
from shop import serializers
from shop import models


def display_image(request, image_name):
    try:
        full_image_path = os.path.join(settings.MEDIA_ROOT, image_name)
        image_data = Image.open(full_image_path)
        response = HttpResponse(content_type="image/jpeg")
        image_data.save(response, format="JPEG")
        return response

    except FileNotFoundError:
        return HttpResponse("Не удается найти изображение", status=404)


class PainterAPI(viewsets.ModelViewSet):
    queryset = models.Painter.objects.all()
    serializer_class = serializers.PainterSer


class PictureAPI(viewsets.ModelViewSet):
    queryset = models.Picture.objects.all()
    serializer_class = serializers.PictureSer


class PictureListView(FilterView):
    template_name = 'picture_shop/pictures_list.html'
    model = Picture
    context_object_name = 'pictures'
    filterset_class = filters.Picture


class PictureDetailView(DetailView):
    template_name = 'picture_shop/pictures_detail.html'
    model = Picture
    context_object_name = 'picture'


class PictureCreateView(CreateView):
    template_name = 'picture_shop/pictures_form.html'
    model = Picture
    context_object_name = 'picture'
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy('pictures_detail', kwargs={'pk': self.object.pk})


class PictureUpdateView(UpdateView):
    template_name = 'picture_shop/pictures_form.html'
    model = Picture
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy('pictures_detail', kwargs={'pk': self.object.pk})


class PictureDeleteView(DeleteView):
    template_name = 'picture_shop/pictures_confirm_delete.html'
    model = Picture
    success_url = reverse_lazy('pictures_list')


class RegisterView(FormView):
    form_class = UserRegisterForm
    template_name = "registration/register.html"

    def get_success_url(self):
        return reverse_lazy('pictures_list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class MyLoginView(LoginView):
    def get_success_url(self):
        return reverse_lazy('pictures_list')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('pictures_list')
    else:
        return redirect('pictures_list')


def profile_view(request):
    return render(request, 'picture_shop/profile.html')


class CartView(LoginRequiredMixin, ListView):
    model = models.CartItem
    template_name = 'picture_shop/cart.html'
    context_object_name = 'cart_items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_price"] = sum(cart_item.picture.price for cart_item in context['cart_items'])
        return context

    def get_queryset(self):
        cart = models.Cart.objects.get_or_create(user=self.request.user)[0]
        return cart.cart_items.all()


class AddToCartView(LoginRequiredMixin, DetailView):
    model = models.Picture
    template_name = 'picture_shop/pictures_detail.html'

    def get(self, request, *args, **kwargs):
        picture = self.get_object()
        cart, created = models.Cart.objects.get_or_create(user=request.user)
        try:
            cart_item = cart.cart_items.get(picture=picture)
            cart_item.save()
        except models.CartItem.DoesNotExist:
            cart_item = models.CartItem.objects.create(cart=cart, picture=picture)
        return redirect('pictures_detail', pk=picture.pk)


class RemoveFromCartView(LoginRequiredMixin, DeleteView):
    model = models.CartItem
    context_object_name = 'cart_item'
    template_name = 'picture_shop/cart_confirm_delete.html'
    success_url = reverse_lazy('cart')

    def get_success_url(self):
        return self.success_url


















