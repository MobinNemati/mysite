from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Post
import datetime, time
from django.utils import timezone
from django.db.models import F


def blog_view(request):
    now1=timezone.now()
    posts = Post.objects.filter(published_date__lt=now1, status=1)
    context = {'posts': posts}
    return render(request, 'blog/blog-home.html', context)


def blog_single(request, pid):
    now=timezone.now()
    posts = get_object_or_404(Post, published_date__lt=now, status=1, id=pid)
    posts.counted_view += 1
    posts.save()

    next_post = Post.objects.filter(published_date__lt=now, status=1, id__gt=pid).order_by('id').first()
    prev_post = Post.objects.filter(published_date__lt=now, status=1, id__lt=pid).order_by('-id').first()

    context = {'posts': posts, 'prev_post': prev_post, 'next_post': next_post}
    return render(request, 'blog/blog-single.html', context)
        

def blog_category(request, cat_name):
    posts = Post.objects.filter(status=1)
    posts = posts.filter(category__name=cat_name)
    context = {'posts':posts}
    return render(request, 'blog/blog-home.html', context)

    
def test(request):
    return render(request, 'test.html')