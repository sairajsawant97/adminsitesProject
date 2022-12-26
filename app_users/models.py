from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
# Create your models here.

from django.db import models
import os
from django.urls import reverse

def path_and_rename(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = 'User_Profile_Pictures/{}.{}'.format(instance.pk, ext)
    return os.path.join(upload_to, filename)


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=155,
        unique=True,
        error_messages={'unique': 'A user with that email already exists.'}, 
        help_text='Required. 150 characters or fewer. Letters, digits and @/./_ only.',
    )
    none = 'None'
    teacheradmin = 'teacheradmin'
    studentadmin = 'studentadmin'
    admin_types = [
        (none, 'None'),
        (teacheradmin, 'teacheradmin'),
        (studentadmin, 'studentadmin'),
    ]
    admin_type = models.CharField(max_length=100, choices=admin_types, default=none)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name'] # removes email from REQUIRED_FIELDS

    manager = UserManager()

    def __str__(self):
        return self.first_name


class UserProfileInfo(models.Model):

    #creating a relationship with user class (not inheriting)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #adding additional attributes
    bio = models.CharField(max_length=500)
    profile_pic = models.ImageField(upload_to=path_and_rename, verbose_name="Profile Picture", blank=True)
    teacher = 'teacher'
    student = 'student'
    parent = 'parent'
    user_types = [
        (teacher, 'teacher'),
        (student, 'student'),
        (parent, 'parent'),
    ]
    teacheradmin = 'teacheradmin'
    studentadmin = 'studentadmin'
    admin_types = [
        (teacheradmin, 'teacheradmin'),
        (studentadmin, 'studentadmin'),
    ]
    admin_type = models.CharField(max_length=100, choices=admin_types, default='None')

    user_type = models.CharField(max_length=10, choices=user_types, default=student)


    def __str__(self):
        return self.user.username

class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    feedback = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('index')

