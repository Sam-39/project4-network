from django.urls import path
from django.views.generic.base import RedirectView
from . import views
from django.urls import re_path

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following", views.following, name="following"),

    path("profile/<str:profile>/follow", views.follow, name="follow"),
    path("profile/<str:profile>/unfollow", views.unfollow, name="unfollow"),


    #API
    # Get a post from diffrent pages
    path("posts/<int:post_id>", views.post, name="post"),
    path("profile/posts/<int:post_id>", views.post, name="profile_post"),
    path("<str:usename>/posts/<int:post_id>", views.post, name="following_post"),
    
    path("posts/all", views.posts, name="posts")
]
