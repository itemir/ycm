from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Member

class MemberAdmin(UserAdmin):
    model = Member 
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active','vessel',)
    list_filter = ('email', 'first_name', 'last_name', 'is_staff', 'is_active','vessel',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal Information', {'fields': ('first_name', 'last_name')}),
        ('Vessel Information', {'fields': ('vessel',)}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active','vessel')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(Member, MemberAdmin)
