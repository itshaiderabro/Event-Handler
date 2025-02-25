from django.urls import path
from .  import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('registration', views.registration_user, name='registration')
]