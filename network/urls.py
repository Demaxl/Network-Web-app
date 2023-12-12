
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("users/<str:username>/", views.profile_view, name="profile"),
    path("following/", views.following_view, name="following-page"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("api/follow", views.toggle_follow, name="api-follow"),
    path("api/edit", views.edit, name="api-edit-post")
]
