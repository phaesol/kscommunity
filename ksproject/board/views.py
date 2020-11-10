from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from .forms import PostForm
from .models import Post,Category,Mini_Category
from django.core.paginator import Paginator
# from django.urls import reverse_lazy




def create(request,mini_category_id): 
    context = dict()
    
    categories = Category.objects.all()   
    context['categories'] = categories    

    mini_category = get_object_or_404(Mini_Category,id=mini_category_id)  
    context['mini_category'] = mini_category

    if request.method=="POST":
        post_form = PostForm(request.POST, request.FILES) 
        
        if post_form.is_valid():
            category_form = post_form.save(commit=False) 
            category_form.category = Mini_Category.objects.get(id=mini_category_id) 
            category_form.save() 
            return redirect('post_list',mini_category_id)
      
    else:
        context['post_form'] = PostForm()
        return render(request,'create.html',context)    


def post_list(request,mini_category_id): #여기서도 각각의 미니카테고리 아이디 가져올거임.
    context=dict()
    
    categories = Category.objects.all()
    context['categories'] = categories  


    mini_category = Mini_Category.objects.get(id=mini_category_id)     #마찬가지로 여기서도 미니카테고리의 id 를 들고와줌.
    context['mini_category'] = mini_category


    category_post_list = Post.objects.filter(category=mini_category)
    context['category_post_list'] =category_post_list                  
    
    paginator = Paginator(category_post_list, 10) # 하나의 페이지당 10개의 오브젝트들을 보여줌.
    page_number = request.GET.get('page') #GET 방식으로 요청한 url의 page 값을 가져와줌.
    page_obj = paginator.get_page(page_number) # 한 페이지당 요청된 갯수만큼의 오브젝트들
    context['page_obj'] = page_obj
    return render(request,'post_list.html',context)



def detail(request,post_id):
    context = dict()

    categories = Category.objects.all()
    context['categories'] = categories

             

    my_post =get_object_or_404(Post,id=post_id)
    context['my_post'] = my_post

    return render(request,'detail.html',context)





