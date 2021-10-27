from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Image(models.Model):
    """Image model class"""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to='media/', null=True, blank=True)
    date_added = models.DateTimeField('Posted on: ', auto_now_add=True)
