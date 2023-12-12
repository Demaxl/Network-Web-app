import json, bleach
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.template import loader

from pprint import pprint
from .models import User, Post, Follow, Comment


def paginate(request, queryset):
    p = Paginator(queryset, 10)

    page_num = request.GET.get("page", 1)
    page_obj = p.get_page(page_num)
    return page_obj


def index(request):
    if request.method == "POST":
        body = request.POST['new-post']
        Post.objects.create(
            poster=request.user,
            body=body
        )
        messages.success(request, "New post created!!")
        return redirect("index")

    return render(request, "network/index.html", {
        "page_obj": paginate(request, Post.objects.all().order_by("-date_time")),
        "headline": "All Posts"
    })


def toggle_follow(request):
    body = json.loads(request.body.decode())
    user = get_object_or_404(User, username=body['username'])

    if body['action'] == "FOLLOW":
        request.user.follow(user)
    else:
        request.user.unfollow(user)

    return JsonResponse({"success": "ok"})

def edit(request):
    body = json.loads(request.body.decode())

    post = get_object_or_404(Post, pk=int(body['postId']))

    if request.user != post.poster:
        return JsonResponse({"error": "Only poster can edit this post"}, status=403)
    
    post.body = bleach.clean(body['postBody'])
    post.save()

    template = loader.get_template("network/post.html")

    return JsonResponse({
        "success": "ok",
        "post": template.render({"post":post, "user":request.user})
        })


def profile_view(request, username):
    user = get_object_or_404(User, username=username)


    return render(request, "network/profile.html", {
        "object": user,
        "page_obj": paginate(request, Post.objects.filter(poster=user).order_by("-date_time")),
        "is_following": request.user.is_following(user) if request.user.is_authenticated else False
    })

@login_required(login_url="login")
def following_view(request):
    return render(request, "network/index.html", {
        "page_obj": paginate(request, Post.objects.filter(poster__in=request.user.get_followings()).order_by("-date_time")),
        "headline": "Following Page"
    })

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(request.POST.get("next"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html", {
            "next": request.GET.get("next", reverse("index"))
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
