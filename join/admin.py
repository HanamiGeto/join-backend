from django.contrib import admin

from join.models import Task, Category, Subtask, Contact

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'color')

class SubtaskAdmin(admin.ModelAdmin):
    list_display = ('done', 'title', 'task')
    

class TaskAdmin(admin.ModelAdmin):
    fields = ('title', 'created_at', 'author', 'assigned_to', 'due_date', 'category', 'urgency', 'process_status', 'description')
    list_display = ('title', 'created_at', 'author', 'assigned_to', 'due_date', 'category_with_color', 'urgency', 'process_status', 'description')
    
    @admin.display(description='category')
    def category_with_color(self, obj):
        return f'{obj.category.title} {obj.category.color}'
    
    @admin.display(description='assigned_to')
    def assigned_to(self, obj):
        return obj.assigned_to.name

admin.site.register(Task, TaskAdmin)
admin.site.register(Category, CategoryAdmin) 
admin.site.register(Subtask, SubtaskAdmin)
admin.site.register(Contact)