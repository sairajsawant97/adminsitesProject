from django.urls import path
from app_users import views
from app_users.admin import teacheradmin, studentadmin


# app_name = 'app_users'
urlpatterns = [
    path('',views.HomeView.as_view(),name='index'),
    path('teacheradmin/', teacheradmin.urls),
    path('studentadmin/', studentadmin.urls),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('contact/', views.ContactView.as_view(), name="contact"),
]