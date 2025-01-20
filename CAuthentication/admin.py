from django.contrib import admin
from django.contrib.auth.models import User

from CAuthentication.models import Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('old_cart',)


admin.site.register(Profile, ProfileAdmin)


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    field = ['username', 'first_name', 'last_name', 'email']
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
