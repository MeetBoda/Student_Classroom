from django.contrib import admin
from classrooms.models import Classrooms

class ClassroomsAdmin(admin.ModelAdmin):
    list_display=('classroom_name',)

admin.site.register(Classrooms, ClassroomsAdmin)

# Register your models here.
