from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from .forms import PostForm,CommentForm,ReCommentForm
from .models import Post,Category,Mini_Category,Comment,ReComment
from django.core.paginator import Paginator
from accounts.models import CommunityUser
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from hitcount.views import HitCountDetailView
from django.views.generic import DeleteView
from django.urls import reverse_lazy,reverse
@login_required
def create(request,mini_category_id): 
    context = dict()
    
    categories = Category.objects.all()   
    context['categories'] = categories    


    if request.method=="POST":
        post_form = PostForm(request.POST, request.FILES) 
        
        if post_form.is_valid():
            post_user = request.user
            user = CommunityUser.objects.get(email=post_user)
            user_nickname = user.nickname
            category_form = post_form.save(commit=False) 
            category_form.category = Mini_Category.objects.get(id=mini_category_id)
            category_form.writer =  user_nickname
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


# @login_required
# def detail(request,post_id):
#     context = dict()
   
   
#     user = request.user
#     categories = Category.objects.all()
#     context['categories'] = categories

#     context['comment_form'] = CommentForm()
#     context['recomment_form'] = ReCommentForm()
             

#     my_post =get_object_or_404(Post,id=post_id)
#     context['my_post'] = my_post
    # session_cookie = request.session['user_id']
    # cookie_name = F'detail_hits:{session_cookie}'

    # if request.COOKIES.get(cookie_name) is not None:
    #     cookies = request.COOKIES.get(cookie_name)
    #     cookie_list = cookies.split('|')
    #     if str(pk) not in cookie_list:
    #         response.set_cookie(cookie_name, cookies + f'|{pk}', expires=None)
    #         my_post.hits +=1
    #         my_post.save()
    #         return response
    # else:
    #         response.set_cookie(cookie_name,pk,expires=None)
    #         my_post.hits += 1
    #         my_post.save()
    #         return response
   
   
    
  
    # return render(request,'detail.html',context)

@login_required
def update_post(request,post_id):
    context = dict()
    
    my_post = Post.objects.get(id=post_id)
    post_form = PostForm(instance=my_post)
    context['post_form'] = post_form
    categories = Category.objects.all()
    context['categories'] = categories


    if request.method == "POST":
        update_form = PostForm(request.POST, request.FILES,instance=my_post) 
        if update_form.is_valid():
            update_form.save()
            return redirect('detail',post_id)
   
    return render(request,'create.html',context)  

# @login_required
# def delete_post(request,post_id):
#     context = dict() 
#     my_post = Post.objects.get(id=post_id)
#     context['my_post'] = my_post
#     user = request.user
#     context['user'] = user
#     my_post.delete()
   
#     return render(request,'detail.html',context)
class deleteView(DeleteView):
    model = Post
    template_name= 'delete_confirm.html'

    def get_success_url(self):
        return reverse('post_list', kwargs={'mini_category_id': self.object.category_id})
    

    

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



@login_required
def create_comment(request,post_id):
    context = dict()
    if request.method == "POST":
        com_form = CommentForm(request.POST)
        if com_form.is_valid():
            com_user = request.user
            user = CommunityUser.objects.get(email=com_user)
            user_nickname = user.nickname
            comment_form = com_form.save(commit=False)
            comment_form.post = Post.objects.get(id=post_id)
            comment_form.writer =  user_nickname
            comment_form.save()

            return redirect('detail',post_id)
    

@login_required
def delete_comment(request,com_id):
    context = dict() 
    my_com = Comment.objects.get(id=com_id)
    context['my_com'] = my_com
    user = request.user
    context['user'] = user
    my_com.delete()
   
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def create_recomment(request,post_id,com_id):
    re_com_form = ReCommentForm(request.POST)
    if re_com_form.is_valid():
        recom_user = request.user
        user = CommunityUser.objects.get(email=recom_user)
        user_nickname = user.nickname
        recomment_form = re_com_form.save(commit=False)
        recomment_form.comment = Comment.objects.get(id=com_id)
        recomment_form.writer =  user_nickname
        recomment_form.save()
    
    return redirect('detail',post_id)


def delete_recomment(request,recom_id):
    context = dict()
    my_recom = ReComment.objects.get(id=recom_id)
   
    context['my_recom'] = my_recom
    user = request.user
    context['user'] = user
   
    my_recom.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def like_toggle(request,post_id):
    context = dict()
    post = get_object_or_404(Post, pk = post_id)
    
    user = request.user
    
    try:
        check_like = user.like_post.get(id=post_id)
        user.like_post.remove(post)
        post.like_count -= 1
        print(post.like_count)
        post.save()
    except:
        user.like_post.add(post)
        post.like_count += 1
        print(post.like_count)
        post.save()
    
    return redirect('detail',post_id)

class PostDetail(HitCountDetailView):

    model = Post
    template_name = 'detail.html'
    count_hit = True
    context_object_name = 'my_post'

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['my_post'] = Post.objects.get(pk=self.object.pk)
        context['categories'] = Category.objects.all()
        context['comment_form'] = CommentForm()
        context['recomment_form'] = ReCommentForm()
        context.update({
            'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3],
        })
        
        return context
	
  