from django.shortcuts import render,get_object_or_404
from django.views.generic import View
from .models import *

# Create your views here.


class PostViews(View):
    def get(self,request):
        id = request.GET.get("id")
        read = get_object_or_404(Posts,id=id)
        return render(request,"article/read_article.html",{"read":read})


class MoreViews(View):
    def get(self,request):
        post = Posts.objects.all()
        return render(request,'article/more.html',{"post":post})
