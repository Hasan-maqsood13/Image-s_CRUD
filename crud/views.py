from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.dateparse import parse_datetime
from django.forms.models import model_to_dict
from django.utils.timezone import make_aware
from django.core.mail import send_mail
from django.utils.text import slugify
from django.core import serializers
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from urllib.parse import unquote
from django.db.models import Sum
from django.urls import reverse
from datetime import timedelta
from datetime import datetime
from .models import *
import random
import stripe
import json
import re


# Create your views here.
def home(request):
    return HttpResponse("Hello, Django is working fine!")

def gallery_view(request):
    if request.method == "POST":
        title = request.POST.get("title")
        images = request.FILES.getlist("images")   # multiple images

        if not title:
            return JsonResponse({"success": False, "message": "Title is required."})

        uploaded_photos = []
        for img in images:
            photo = Photo.objects.create(title=title, image=img)
            uploaded_photos.append({
                "id": photo.id,
                "title": photo.title,
                "image_url": photo.image.url,
                "created_at": photo.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })

        return JsonResponse({"success": True, "photos": uploaded_photos})

    photos = Photo.objects.all().order_by('-created_at')
    return render(request, "gallery.html", {"photos": photos})


def delete_photo(request, pk):
    if request.method == "POST":
        try:
            photo = Photo.objects.get(pk=pk)
            photo.delete()
            return JsonResponse({"success": True, "message": "Photo deleted successfully."})
        except Photo.DoesNotExist:
            return JsonResponse({"success": False, "message": "Photo not found."})
    return JsonResponse({"success": False, "message": "Invalid request."})

def edit_photo(request, pk):
    if request.method == "POST":
        try:
            photo = Photo.objects.get(pk=pk)

            title = request.POST.get("title")
            new_image = request.FILES.get("image")

            if title:
                photo.title = title
            if new_image:  # agar user nayi image upload kare
                photo.image = new_image

            photo.save()

            return JsonResponse({
                "success": True,
                "message": "Photo updated successfully.",
                "photo": {
                    "id": photo.id,
                    "title": photo.title,
                    "image_url": photo.image.url,
                    "created_at": photo.created_at.strftime("%Y-%m-%d %H:%M:%S")
                }
            })
        except Photo.DoesNotExist:
            return JsonResponse({"success": False, "message": "Photo not found."})

    return JsonResponse({"success": False, "message": "Invalid request."})
