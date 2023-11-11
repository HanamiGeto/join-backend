import datetime
from django.conf import settings
from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Create your models here.
URGENCY = (('low', 'Low'),
           ('med', 'Medium'),
           ('high', 'High'))

# creates a list with all the registered user
USERS_CHOICES = [(user.id, user.username) for user in User.objects.all()]

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=12)

class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.name}'
    
class Subtask(models.Model):
    checked = models.BooleanField(default=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'

class Task(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        blank=True,
        null=True,
    )
    created_at = models.DateField(default=datetime.date.today)
    assigned_contacts = MultiSelectField(
        choices=USERS_CHOICES,
        blank=True,
        max_length=300)
    due_date = models.DateField(default=None)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    urgency = models.CharField(max_length=6, choices=URGENCY)
    description = models.CharField(max_length=300)
    # subtask = models.CharField(max_length=100, blank=True)
    subtask = models.ForeignKey(
        Subtask,
        on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.id} {self.title}'