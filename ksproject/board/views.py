from django.shortcuts import render,redirect,get_object_or_404
from .forms import PostForm
from .models import Post,Category,Mini_Category
from django.core.paginator import Paginator
# from django.urls import reverse_lazy




def create(request,mini_category_id): #우리가 가져올 mini_category 값 가져와 주기
    context = dict() 

    categories = Category.objects.all()   # 전체 카테고리를 오브젝트로 들고와서 템플릿에 네브바로 띄워주기 위해
    context['categories'] = categories    #이것은 템플릿 상속을 받아온 base.html 에 쓸 거임.

    mini_categories = Mini_Category.objects.all() # 마찬가지로 미니카테고리도 들고 와줌. 마찬가지로 얘도 base.html에서 씀.
    context['mini_categories'] = mini_categories

    mini_category = Mini_Category.objects.get(id=mini_category_id)     #작성 게시판 이름으로 써줄 거임.
    context['mini_category'] = mini_category

    if request.method=="POST":
        post_form = PostForm(request.POST, request.FILES) # POST 요청으로 들어오면 미디어파일도 있기 때문에, request.FILES 도 같이 추가
        
        if post_form.is_valid(): #폼 유효성 검사
            category_form = post_form.save(commit=False)  #저장 지연
            category_form.category = Mini_Category.objects.get(id=mini_category_id) #저장하기전에 아이디 값 category 필드에 같이 넘겨서 
            category_form.save() #아이디값 가진 채 저장
            return redirect('post_list',mini_category_id) # redirect로 post_list/mini_category_id 이렇게 url 뒤에 id 지정해서 붙여줌.

        else:
            context['post_form'] = PostForm()
            return render(request,'create.html',context) # 폼 유효성 검사 실패시 
    else:
        context['post_form'] = PostForm()
        return render(request,'create.html',context)     # GET 방식으로 요청 들어올시


def post_list(request,mini_category_id): #여기서도 각각의 미니카테고리 아이디 가져올거임.
    context=dict()
    
    categories = Category.objects.all()
    context['categories'] = categories   #위에처럼 카테고리,미니 카테고리 네브바에 띄워줄 객체들 여기서도 들고와야함.

    mini_categories = Mini_Category.objects.all()
    context['mini_categories'] = mini_categories  
    
    mini_category = Mini_Category.objects.get(id=mini_category_id)     #마찬가지로 여기서도 미니카테고리의 id 를 들고와줌.
    context['mini_category'] = mini_category


    category_post_list = Post.objects.filter(category=mini_category)   # Post 모델의 카테고리 필드에서 위의 mini_category 
    context['category_post_list'] =category_post_list                  # 즉 , 해당 미니카테고리의 아이디인 것만 필터링
 
    # paginator = Paginator(free_post_list, 10) # 하나의 페이지당 10개의 오브젝트들을 보여줌.
    # page_number = request.GET.get('page') #GET 방식으로 요청한 url의 page 값을 가져와줌.
    # page_obj = paginator.get_page(page_number) # 한 페이지당 요청된 갯수만큼의 오브젝트들
    # context['page_obj'] = page_obj
    return render(request,'post_list.html',context)



