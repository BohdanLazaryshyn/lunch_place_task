import os
import uuid

from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from user.models import User


def upload_file_path(instance, filename):
    _, ext = os.path.splitext(filename)
    if ext in (".jpeg", ".jpg", ".png", ".pdf"):
        filename = f"{slugify(instance.name)}-{uuid.uuid4()}"
        return os.path.join(f"uploads/{instance}/", filename + ext)
    raise ValueError("Unsupported file type")


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to=upload_file_path, blank=True, null=True
    )

    @property
    def full_name(self):
        return f"{self.name} {self.last_name}"


class Restaurant(models.Model):
    TEXT_PREVIEW_LENGTH = 30

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True)
    rest_picture = models.ImageField(
        upload_to=upload_file_path, blank=True, null=True
    )

    @property
    def description_preview(self):
        if len(self.description) <= self.TEXT_PREVIEW_LENGTH:
            return self.description
        return self.description[:self.TEXT_PREVIEW_LENGTH] + "..."

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menus"
    )
    date = models.DateField(default=timezone.now)
    menu_items = models.TextField(max_length=500)
    today_menu = models.FileField(
        upload_to=upload_file_path, blank=True, null=True
    )

    class Meta:
        unique_together = ("restaurant", "date")

    @property
    def total_votes(self):
        return self.votes.count()

    @property
    def name(self):
        return self.restaurant.name + " " + str(self.date)


class Vote(models.Model):
    user = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="votes"
    )
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name="votes"
    )

    def __str__(self):
        return f"{self.user.full_name} voted for {self.menu.restaurant} - {self.menu.date}"
