from django.http import HttpResponse
from PIL import Image
from django.conf import settings
import os
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from shop import filters
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
    fields = ['title', 'history', 'price', 'is_original', 'availability']

    def get_success_url(self):
        return reverse_lazy('pictures_detail', kwargs={'pk': self.object.pk})


class PictureUpdateView(UpdateView):
    template_name = 'picture_shop/pictures_form.html'
    model = Picture
    fields = ['title', 'history']

    def get_success_url(self):
        return reverse_lazy('pictures_detail', kwargs={'pk': self.object.pk})


class PictureDeleteView(DeleteView):
    template_name = 'picture_shop/pictures_confirm_delete.html'
    model = Picture
    success_url = reverse_lazy('pictures_list')
