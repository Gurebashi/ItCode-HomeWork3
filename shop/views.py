from django.http import HttpResponse
from django.shortcuts import render
from PIL import Image
from django.conf import settings
import os


def display_image(request, image_name):
    try:
        full_image_path = os.path.join(settings.MEDIA_ROOT, image_name)
        image_data = Image.open(full_image_path)
        response = HttpResponse(content_type="image/jpeg")
        image_data.save(response, format="JPEG")
        return response

    except FileNotFoundError:
        return HttpResponse("Не удается найти изображение", status=404)
