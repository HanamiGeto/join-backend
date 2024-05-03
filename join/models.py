import datetime
from django.conf import settings
from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=12)
    initials = models.CharField(max_length=100)
    initials_color = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    title = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title


class Task(models.Model):
    URGENCY = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    )

    PRIORITY_STATUS = (
        ('to-do', 'To do'),
        ('in-progress', 'In progress'),
        ('await-feedback', 'Await feedback'),
        ('done', 'Done')
    )

    title = models.CharField(max_length=100, blank=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        blank=True,
        null=True,
    )
    created_at = models.DateField(default=datetime.date.today)
    assigned_to = models.ManyToManyField(
        Contact,
        symmetrical=False,
        related_name='assigned_to'
    )
    due_date = models.DateField(blank=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='category'
    )
    urgency = models.CharField(
        max_length=6, 
        choices=URGENCY,
        blank=True
    )
    process_status = models.CharField(
        max_length=16,
        choices=PRIORITY_STATUS,
        default='to-do'
    )
    description = models.CharField(max_length=300, blank=True)
    
    def __str__(self):
        return f'{self.id} {self.title}'
    
class Subtask(models.Model):
    title = models.CharField(max_length=100)
    done = models.BooleanField(default=False)
    task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE, 
        related_name='subtasks'
    )

    def __str__(self):
        return f'{self.id} {self.title}'