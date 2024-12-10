import scrumble_site.views as views
from extensions.game import index
from extensions.social import profile_system
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('register/', views.register_root, name='register'),
    path('login', views.login_root, name='login'),
    path('profile/<int:uid>/', profile_system, name='profile')
]
