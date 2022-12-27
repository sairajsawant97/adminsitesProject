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
    # login_form = AuthenticationForm

    # def has_permission(self, request):
    #     """
    #     Checks if the current user has access.
    #     """
    #     return request.user.admin_type=='None'



admin.site.register(UserProfileInfo)


class MultiDBModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


class MultiDBModelAdmin1(MultiDBModelAdmin):
    # A handy constant for the name of the alternate database.
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
    using = 'teachers'



class MultiDBModelAdmin2(MultiDBModelAdmin):
    # A handy constant for the name of the alternate database.
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
    using = 'students'


class TeacherAdminSite(AdminSite):
    #login_form = AuthenticationForm

    site_header = 'Admin For Teachers'

    login_form = AuthenticationForm
    def has_permission(self, request):
        """
        Checks if the current user has access.
        """
        if request.user.is_anonymous:
            pass
        else:
            return request.user.admin_type=='teacheradmin'

    # def has_permission(self, request):
    #     """
    #     Checks if the current user has access.
    #     """
    #     return request.user.is_active

teacheradmin = TeacherAdminSite(name='teacheradmin')
teacheradmin.register(Standard)
teacheradmin.register(Subject)
teacheradmin.register(Lesson)
teacheradmin.register(TimeSlots)
teacheradmin.register(SlotSubject)

class StudentAdminSite(AdminSite):
    # login_form = AuthenticationForm

    site_header = 'Admin For Students'


    login_form = AuthenticationForm
    def has_permission(self, request):
        """
        Checks if the current user has access.
        """
        if request.user.is_anonymous:
            pass
        else:
            return request.user.admin_type=='studentadmin'
            

    # def has_permission(self, request):
    #     """
    #     Checks if the current user has access.
    #     """
    #     return request.user.admin_type=='studentadmin'

studentadmin = StudentAdminSite(name='studentadmin')
studentadmin.register(Subject)
studentadmin.register(Lesson)

teacheradmin.register(User, MultiDBModelAdmin1)

studentadmin.register(User, MultiDBModelAdmin2)