from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from board.forms import PostForm,CommentForm,ReCommentForm
from board.models import Post,Category,Mini_Category,Comment,ReComment

def index(request):
    context = dict()
    
    categories = Category.objects.all()
    context['categories'] = categories

   
    mini_1 = Mini_Category.objects.get(id=1)
    context['mini_1'] = mini_1
    post_1 = Post.objects.filter(category=mini_1).order_by('-id')[:5]
    context['post_1']=post_1
  
    mini_2 = Mini_Category.objects.get(id=2)
    context['mini_2'] = mini_2
    post_2 = Post.objects.filter(category=mini_2).order_by('-id')[:5]
    context['post_2']=post_2

    mini_5 = Mini_Category.objects.get(id=5)
    context['mini_5'] = mini_5
    post_5 = Post.objects.filter(category=mini_5).order_by('-id')[:5]
    context['post_5']=post_5

    mini_8 = Mini_Category.objects.get(id=8)
    context['mini_8'] = mini_8
    post_8 = Post.objects.filter(category=mini_8).order_by('-id')[:5]
    context['post_8']=post_8


    mini_9 = Mini_Category.objects.get(id=9)
    context['mini_9'] = mini_9
    post_9 = Post.objects.filter(category=mini_9).order_by('-id')[:5]
    context['post_9']=post_9

    mini_13 = Mini_Category.objects.get(id=13)
    context['mini_13'] = mini_13
    post_13 = Post.objects.filter(category=mini_13).order_by('-id')[:5]
    context['post_13']=post_13

    context['popular_posts'] = Post.objects.order_by('-hit_count_generic__hits')[:10]





  


    return render(request,'index.html',context)



   



