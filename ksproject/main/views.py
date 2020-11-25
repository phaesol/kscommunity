from django.shortcuts import render,redirect
from board.models import Category,Mini_Category,Post
from django.core.paginator import Paginator


def index(request):
    context = dict()
    
    categories = Category.objects.all()
    context['categories'] = categories

   

 
  

    return render(request,'index.html',context)







