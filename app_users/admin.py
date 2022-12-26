from django.contrib import admin
from app_users.models import UserProfileInfo
from django.contrib.admin import AdminSite
from curriculum.models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin.forms import AuthenticationForm

# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("first_name", "last_name", "email", "password1", "password2", 
                "admin_type"),
            },
        ),
    )

    list_display = ("email", "first_name", "last_name", "is_staff", "admin_type")
    list_editable = ["admin_type"]
    login_form = AuthenticationForm

    def has_permission(self, request):
        """
        Checks if the current user has access.
        """
        return request.user.admin_type=='None'


admin.site.register(UserProfileInfo)

class TeacherAdminSite(AdminSite):
    login_form = AuthenticationForm

    site_header = 'Admin For Teachers'

    def has_permission(self, request):
        """
        Checks if the current user has access.
        """
        return request.user.admin_type=='teacheradmin'

teacheradmin = TeacherAdminSite(name='teacheradmin')
teacheradmin.register(Standard)
teacheradmin.register(Subject)
teacheradmin.register(Lesson)
teacheradmin.register(TimeSlots)
teacheradmin.register(SlotSubject)

class StudentAdminSite(AdminSite):
    login_form = AuthenticationForm

    site_header = 'Admin For Students'

    def has_permission(self, request):
        """
        Checks if the current user has access.
        """
        return request.user.admin_type=='studentadmin'

studentadmin = StudentAdminSite(name='studentadmin')
studentadmin.register(Subject)
studentadmin.register(Lesson)