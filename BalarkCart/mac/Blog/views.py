from django.shortcuts import render
from .models import Blogpost
# from django.http import HttpResponse

def index(request):
    mypost = Blogpost.objects.all()
    return render(request,'Blog/index.html',{'mypost':mypost})

def blogpost(request,id):
    post = Blogpost.objects.filter(post_id = id)[0]
    return render(request,'Blog/blogpost.html',{'post':post})