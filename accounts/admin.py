from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin # we are importing the user admin here


# Register your models here.
class CustomUserAdmin(UserAdmin): # this class is making the password field non editable, we can read only
    list_display = ('email', 'first_name', 'last_name', 'username', 'roles', 'is_active')
    ordering = ('-date_joined',) # always provide a comma if we have only one value in the tuple
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, CustomUserAdmin) # this adds the user field in the /admin
admin.site.register(UserProfile)