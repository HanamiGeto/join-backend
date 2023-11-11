from django.contrib import admin

from join.models import Task, Category, Subtask

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')

class SubtaskAdmin(admin.ModelAdmin):
    list_display = ('checked', 'name')

class TaskAdmin(admin.ModelAdmin):
    fields = ('title', 'created_at', 'author', 'assigned_contacts', 'due_date', 'category', 'urgency', 'description', 'subtask')
    list_display = ('title', 'created_at', 'author', 'assigned_contacts', 'due_date', 'category_with_color', 'urgency', 'description', 'checkbox_with_subtask')
    
    @admin.display(description="category")
    def category_with_color(self, obj):
        return f"{obj.category.name} {obj.category.color}"
    
    @admin.display(description="subtask")
    def checkbox_with_subtask(self, obj):
        return f"{obj.subtask.checked} {obj.subtask.name}"

admin.site.register(Task, TaskAdmin)
admin.site.register(Category, CategoryAdmin) # or @admin.register(Category) to register
admin.site.register(Subtask, SubtaskAdmin)