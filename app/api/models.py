from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Image(models.Model):
    """Image model class"""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(null=True, blank=True)
    description = models.CharField(max_length=150)
    views = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField('Posted on: ', auto_now_add=True)

    def __str__(self) -> str:
        return self.description
