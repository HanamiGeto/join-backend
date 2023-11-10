import datetime
from django.conf import settings
from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Create your models here.
# ASSIGNED_CONTACTS
URGENCY = (('low', 'Low'),
           ('med', 'Medium'),
           ('high', 'High'))

USERS_CHOICES = [(user.id, user.username) for user in User.objects.all()]

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=12)

class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)

class Task(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        blank=True,
        null=True,
    )
    created_at = models.DateField(default=datetime.date.today)
    assigned_contacts = MultiSelectField(choices=USERS_CHOICES, blank=True, max_length=300)
    due_date = models.DateField(default=None)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    urgency = models.CharField(max_length=6, choices=URGENCY)
    description = models.CharField(max_length=300)
    subtask = models.CharField(max_length=100, blank=True)