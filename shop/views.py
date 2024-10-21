from audioop import reverse
from lib2to3.fixes.fix_input import context

from django.http import HttpResponse
from django.shortcuts import render, redirect
from PIL import Image
from django.conf import settings
import os

from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from unicodedata import category

from shop import filters
from shop.models import Picture

def display_image(request, image_name):
    try:
        full_image_path = os.path.join(settings.MEDIA_ROOT, image_name)
        image_data = Image.open(full_image_path)
        response = HttpResponse(content_type="image/jpeg")
        image_data.save(response, format="JPEG")
        return response

    except FileNotFoundError:
        return HttpResponse("Не удается найти изображение", status=404)


class PictureListView(FilterView):
    template_name = 'picture_shop/pictures_list.html'
    model= Picture
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
    fields= ['title','history','price','is_original','availability']
    def get_success_url(self):
       return reverse_lazy('pictures_detail',kwargs={'pk':self.object.pk})

class PictureUpdateView(UpdateView):
    template_name = 'picture_shop/pictures_form.html'
    model = Picture
    fields= ['title','history']

    def get_success_url(self):
        return reverse_lazy('pictures_detail',kwargs={'pk':self.object.pk})

class PictureDeleteView(DeleteView):
    template_name = 'picture_shop/pictures_confirm_delete.html'
    model = Picture
    success_url=reverse_lazy('pictures_list')

