from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from market_place.models import Profile
from .models import Post
from django.http import HttpResponseForbidden

def reel_index(request):
    """Allow everyone to view posts, but only sellers can post."""
    
    if request.method == "POST":
        if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.user_type == 'seller':
            title = request.POST.get('title', '').strip()
            content = request.POST.get('content', '').strip()
            image = request.FILES.get('image')

            if title and content and image:
                Post.objects.create(
                    title=title,
                    content=content,
                    image=image,
                    author=request.user
                )
                return redirect('reel_index')

    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'reel.html', {'posts': posts})

@login_required
def delete_post(request, post_id):
    """Allow only post authors to delete their posts."""
    post = get_object_or_404(Post, id=post_id)

    if request.user == post.author:
        post.delete()
        return redirect('reel_index')
    else:
        return HttpResponseForbidden("You are not allowed to delete this post.")

def index(request):
    return render(request, 'index.html')
