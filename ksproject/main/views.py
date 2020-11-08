from django.shortcuts import render,redirect
from board.models import Category,Mini_Category


def index(request,category_id):
    context = dict()

    categories = Category.objects.all()
    context['categories'] = categories

    mini_category_group = Category.objects.get(id=category_id)
    mini_category = Mini_Category.objects.all()
    context['mini_categories'] = mini_categories
    
    return render(request,'index.html', context)


