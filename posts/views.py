from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count
from .models import Post, Comment, Vote, UserProfile
from .forms import PostForm, CommentForm

def home(request):
    """Homepage showing top posts"""
    posts = Post.objects.all().annotate(
        comment_count=Count('comments')
    )
    return render(request, 'posts/home.html', {'posts': posts})


def new_posts(request):
    """Show newest posts"""
    posts = Post.objects.all().order_by('-created_at').annotate(
        comment_count=Count('comments')
    )
    return render(request, 'posts/home.html', {
        'posts': posts,
        'page_title': 'New Posts'
    })


def post_detail(request, post_id):
    """Show post details with comments"""
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.filter(parent=None)  # Only top-level comments
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': CommentForm() if request.user.is_authenticated else None,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def submit_post(request):
    """Submit new post form"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post submitted successfully!')
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm()
    
    return render(request, 'posts/submit_post.html', {'form': form})


def user_profile(request, username):
    """Show user profile with their posts and comments"""
    user = get_object_or_404(User, username=username)
    profile = user.profile
    user_posts = user.posts.all()[:10]  # Latest 10 posts
    user_comments = user.comments.all()[:10]  # Latest 10 comments
    
    context = {
        'profile_user': user,
        'profile': profile,
        'user_posts': user_posts,
        'user_comments': user_comments,
    }
    return render(request, 'posts/user_profile.html', context)

def signup(request):
    """User registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})
