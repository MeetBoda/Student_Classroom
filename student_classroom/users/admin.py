from django.contrib import admin
from users.models import Users

class UsersAdmin(admin.ModelAdmin):
    list_display=('user_id','name', 'email', 'role')

admin.site.register(Users, UsersAdmin)

# Register your models here.
