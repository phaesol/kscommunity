from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from .forms import PostForm,CommentForm,ReCommentForm
from .models import Post,Category,Mini_Category,Comment,ReComment
from django.core.paginator import Paginator





def create(request,mini_category_id): 
    context = dict()
    
    categories = Category.objects.all()   
    context['categories'] = categories    


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


def post_list(request,mini_category_id):
    context=dict()
    
    categories = Category.objects.all()
    context['categories'] = categories  


    mini_category = Mini_Category.objects.get(id=mini_category_id)     #마찬가지로 여기서도 미니카테고리의 id 를 들고와줌.
    context['mini_category'] = mini_category


    category_post_list = Post.objects.filter(category=mini_category).order_by('-id')
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

   
    
    context['comment_form'] = CommentForm()
    context['recomment_form'] = ReCommentForm()

    return render(request,'detail.html',context)

def search(request):
    context = dict()

    categories = Category.objects.all()
    context['categories'] = categories

    

    post_list = Post.objects.all().order_by('-id')
    
    
    search_keyword = request.GET.get("result","")

    if search_keyword :
        
        post_list = post_list.filter(title__icontains = search_keyword) | post_list.filter(content__icontains = search_keyword)
        
        paginator = Paginator(post_list, 10)
        page_number = request.GET.get('page') 
        page_obj = paginator.get_page(page_number) 
        context['page_obj'] = page_obj
        context['post_list'] = post_list
        context ['search_keyword'] = search_keyword
        return render(request,'search.html',context)
       
    else:
        return render(request,'search.html',context)




def create_comment(request,post_id):
    com_form = CommentForm(request.POST)
    if com_form.is_valid():
        comment_form = com_form.save(commit=False)
        comment_form.post = Post.objects.get(id=post_id)
        comment_form.save()
    
    return redirect('detail',post_id)


def delete_comment(request,post_id,com_id):
    
    my_com = Comment.objects.get(id=com_id)
    my_com.delete()
    return redirect('detail',post_id)



def create_recomment(request,post_id,com_id):
    re_com_form = ReCommentForm(request.POST)
    if re_com_form.is_valid():
        recomment_form = re_com_form.save(commit=False)
        recomment_form.comment = Comment.objects.get(id=com_id)
        recomment_form.save()
    
    return redirect('detail',post_id)


def delete_recomment(request,post_id,com_id):
    my_recom = ReComment.objects.get(id=com_id)
    my_recom.delete()
    return redirect('detail',post_id)