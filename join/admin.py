from django.contrib import admin

from join.models import Task

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    fields = ('title', 'created_at', 'author', 'assigned_contacts', 'due_date', 'category', 'urgency', 'description', 'subtask')
    list_display = ('title', 'created_at', 'author', 'assigned_contacts', 'due_date', 'category', 'urgency', 'description', 'subtask')
    # search_fields = ('title')


admin.site.register(Task, TaskAdmin)