from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect
from .models import Post, Comment
import datetime, time
from django.utils import timezone
from django.db.models import F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from website.forms import ContactForm
from blog.forms import CommentForm
from django.contrib import messages
from django.urls import reverse



def blog_view(request, cat_name=None, author_username=None, tag_name=None):
    now1=timezone.now()
    posts = Post.objects.filter(published_date__lt=now1, status=1)
    if cat_name:
        posts = posts.filter(category__name=cat_name)
    if author_username:
        posts = posts.filter(author__username=author_username)
    if tag_name:
        posts = posts.filter(tags__name__in=[tag_name])
        
    posts = Paginator(posts, 3)
    try:
        page_number = request.GET.get('page')
        posts = posts.get_page(page_number)
    except PageNotAnInteger:
        posts = posts.get_page(1)
    except EmptyPage:
        posts = posts.get_page(1)
    context = {'posts': posts}
    return render(request, 'blog/blog-home.html', context)


def blog_single(request, pid):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'your commnet submitted successfully')
        else:
            messages.error(request, 'your commnet didnt submited')

    now=timezone.now()
    posts = get_object_or_404(Post, published_date__lt=now, status=1, id=pid)
    posts.counted_view += 1
    posts.save()
    
    if not posts.login_require:
        comments = Comment.objects.filter(post=posts.id, approved=True)

        next_post = Post.objects.filter(published_date__lt=now, status=1, id__gt=pid).order_by('id').first()
        prev_post = Post.objects.filter(published_date__lt=now, status=1, id__lt=pid).order_by('-id').first()
        form = CommentForm()
        context = {'posts': posts, 'prev_post': prev_post, 'next_post': next_post, 'comments': comments, 'form':form}
        return render(request, 'blog/blog-single.html', context)
    
    if posts.login_require is not None:
        if request.user.is_authenticated:
            comments = Comment.objects.filter(post=posts.id, approved=True)
            
            next_post = Post.objects.filter(published_date__lt=now, status=1, id__gt=pid).order_by('id').first()
            prev_post = Post.objects.filter(published_date__lt=now, status=1, id__lt=pid).order_by('-id').first()
            form = CommentForm()
            context = {'posts': posts, 'prev_post': prev_post, 'next_post': next_post, 'comments': comments, 'form':form}
            return render(request, 'blog/blog-single.html', context) 
        else:
            return HttpResponseRedirect(reverse('accounts:login'))   

    
def blog_search(request):
    posts = Post.objects.filter(status=1)
    if request.method == 'GET':
        if s := request.GET.get('s'):
            posts = posts.filter(content__contains=s)
    context = {'posts': posts}
    return render(request, 'blog/blog-home.html', context)    


def test(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('ok')
        else:
            return HttpResponse('not valid')

    form = ContactForm()
    return render(request, 'test.html', {'form':form})