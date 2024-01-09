from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from blog.models import Post
from website.forms import ContactForm, NewsletterForm
from django.contrib import messages


def index_view(request):
   return render(request, 'website/index.html')

def about_view(request):
    return render(request, 'website/about.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            change = form.save(commit=False)
            change.name = 'unknown'
            change.save()
            messages.success(request, 'your ticket submited successfully')
        else:
            messages.error(request, 'your ticket didnt submited')
        
    form = ContactForm()
    return render(request, 'website/contact.html', {'form':form})


def newsletter_view(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'your newsletter submited successfully')
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'your newsletter didnt submited')
            return HttpResponseRedirect('/')

