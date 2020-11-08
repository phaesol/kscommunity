from django.shortcuts import render,redirect
from board.models import Category,Mini_Category


def index(request):
    context = dict()

    categories = Category.objects.all()
    context['categories'] = categories


    mini_categories = Mini_Category.objects.all()
    context['mini_categories'] = mini_categories
    
    return render(request,'index.html', context)


