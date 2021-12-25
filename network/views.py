import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Post, User
from django.core.paginator import Paginator


def index(request):
    # Authenticated users view all posts
    if request.user.is_authenticated:
        if request.method == "POST":
            content = request.POST["content"]
            poster = request.user
            new_post = Post(poster=poster, content=content)
            new_post.save()

        posts = Post.objects.all()
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "network/index.html", {
            "posts": posts,
            'page_obj': page_obj
        })
    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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


@login_required
def profile(request, username):
    profile = User.objects.get(username=username)
    posts = profile.posts.all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        'profile': profile,
        'posts': posts,
        'is_following': profile in request.user.following.all(),
        'page_obj': page_obj
    })


@login_required
def following(request):
    user = request.user
    posts = Post.objects.filter(poster__followers=user).all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        'user': user,
        'following': user.following.all(),
        'posts': posts,
        'page_obj': page_obj
    })


# Post API
@csrf_exempt
@login_required
def post(request, post_id, **usename):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Like/Unlike Post
    if request.method == "PUT":
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            post.save()
            return JsonResponse({"message": f"Post id-{post_id} Unliked."}, status=201)
        else:
            post.likes.add(request.user)
            post.save()
            return JsonResponse({"message": f"Post id-{post_id} Liked."}, status=201)

    # Update Post
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("content", "")

        post.content = content
        post.save()

        return JsonResponse({"message": f"Post id-{post_id} Updated successfully."}, status=201)


# All posts API
@csrf_exempt
@login_required
def posts(request):
    posts = Post.objects.all()
    if request.method == "GET":
        posts = posts.order_by("-timestamp").all()
        return JsonResponse([post.serialize() for post in posts], safe=False)


def follow(request, profile):
    profile = User.objects.get(username=profile)
    user = request.user
    if request.method == "POST":
        user.following.add(profile)
    return HttpResponseRedirect(reverse("profile", args=(profile,)))


def unfollow(request, profile):
    profile = User.objects.get(username=profile)
    user = request.user
    if request.method == "POST":
        user.following.remove(profile)
    return HttpResponseRedirect(reverse("profile", args=(profile,)))
