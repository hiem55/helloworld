from django.contrib import admin

# Register your models here.
from .models import ToDoList
admin.site.register(ToDoList)
from .models import Item
admin.site.register(Item)
