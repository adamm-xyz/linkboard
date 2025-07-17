from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new/', views.new_posts, name='new_posts'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('submit/', views.submit_post, name='submit_post'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]
