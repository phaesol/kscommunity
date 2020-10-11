from django.shortcuts import render,redirect,get_object_or_404
from .forms import PostForm,CommentForm
from .models import Post,Comment
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator


def free(request):
    context=dict()
    free_post_list = Post.objects.filter(category__icontains="자유 게시판").order_by('-id') #id 값순대로 내림차순
    paginator = Paginator(free_post_list, 10) # 하나의 페이지당 10개의 오브젝트들을 보여줌.
    page_number = request.GET.get('page') #GET 방식으로 요청한 url의 page 값을 가져와줌.
    page_obj = paginator.get_page(page_number) # 한 페이지당 요청된 갯수만큼의 오브젝트들
    context['page_obj'] = page_obj
    return render(request,'free.html',context)


def free_detail(request,post_id):
    context = dict()
    
    my_post = get_object_or_404(Post,pk=post_id) #해당 id 값의 게시물 띄워주기
    comment_form = CommentForm()                 #모델폼 변수에 담아주기
    context['my_post'] = my_post                 
    context['comment_form'] = comment_form       #가져올 값들 context에 딕셔너리 형태로 담아주기
    return render(request,'detail.html',context)

def free_update(request,post_id):
    my_post = get_object_or_404(Post,pk=post_id)
    post_form = PostForm(instance = my_post)
    if request.method == "POST":
        update_form =  PostForm(request.POST, instance = my_post)
        if update_form.is_valid():
            update_form.save()
            return redirect('free_detail',post_id)
    return render(request, 'create.html',{'post_form':post_form})


def free_delete(request,post_id):
    my_post = get_object_or_404(Post,pk=post_id)
    my_post.delete()
    return redirect('free')
    
def create_comment(request,post_id):
    filled_form = CommentForm(request.POST) #POST 요청이 들어오면, 
    if filled_form.is_valid(): #유효성 검사에 성공하면, if문 실행. 실패하면 다시 detail로 redirect해서 입력받게 함.
        temp_form = filled_form.save(commit=False)  #category처럼 어떤 id의 글에 저장하는지 명시해주기 위해 잠시 저장 미룸. 
        temp_form.post = Post.objects.get(id = post_id) #참조하는 FK의 값이 어떤 id 값을 받는지 명시
        temp_form.save()                                #저장!

    return redirect('free_detail',post_id)  #실패시 다시 redirect!

def free_create(request):


    context = dict()

    

    if request.method == "POST"  :
        field_form = PostForm(request.POST, request.FILES)
        if field_form.is_valid():
            temp_form = field_form.save(commit = False)  
            temp_form.category ="자유 게시판"  
            temp_form.save()
        return redirect('free')          
    context['post_form'] = PostForm()
    return render(request,'create.html',context)


def private(request):
    context=dict()
    private_post = Post.objects.filter(category__icontains="익명 게시판")
    context['private_post'] = private_post
    return render(request,'private.html',context)


def private_create(request):
    context = dict()
    field_form = PostForm(request.POST, request.FILES)
    if request.method == "POST":
        if field_form.is_valid():
            temp_form = field_form.save(commit=False)
            temp_form.category = "익명 게시판"
            temp_form.save()
        return redirect('private')
    
    
    context['post_form'] = PostForm
    return render(request,'create.html',context)

def search(request):
    context = dict()
    free_post = Post.objects.filter(category__icontains="자유 게시판").order_by('-id') #id 값대로 내림차순한 값과, 자유 게시판에 적힌 글들만 불러와줌.
    post = request.POST.get('post',"") # POST 요청에 따라 인자중에, post 값이 있으면 가져오고, 아니면 빈 문자열 리턴 
    if post:
        free_post = free_post.filter(title__icontains=post) #post가 있으면, title에서 post 내용이 있는 것만 띄워줌.
        context['free_post'] = free_post
        context['post'] = post
        return render(request,'search.html',context)        # post와 post가 포함된 오브젝트들을 딕셔너리형태로 불러와줌.
    else:
        return render(request,'search.html')               # 해당 post 내용이 없으면, search.html 렌더
        

# class PrivateUpdate(UpdateView):
#     model = Post
#     fields = ['title','content','myimage',]
#     template_name = 'update.html'
#     context_object_name = 'update_object'
    



# # def sell(request):
#     context=dict()
#     private_post =Post.objects.filter(category__contains="장터 게시판")
#     context['private_post'] = private_post
#     return render(request,'private.html',context)


# def sell_create(request):
#     context = dict()
#     if request.method == "POST"  :
#         field_form =PostForm(request.POST, request.FILES)
#         if field_form.is_valid():
#             field_form.save()
#         return redirect('free')
#     post_form = PostForm
#     context['post_form'] = post_form
#     return render(request,'create.html',context)

