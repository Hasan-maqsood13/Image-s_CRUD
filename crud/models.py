from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.db.models import CharField, DateField, DecimalField, ImageField
import uuid

# Create your models here.
class Photo(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="gallery/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
