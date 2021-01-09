# import jwt
import json


from django.shortcuts import render,redirect
from django.conf import settings
from django.urls import reverse_lazy
from django.shortcuts import resolve_url, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site


from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView

from .forms import SignUpForm, LoginForm, NicknameUpdateForm,MyPasswordResetForm,NewPasswordSetForm
from .models import CommunityUser
from board.models import Post,Mini_Category,Category

from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import auth,messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
) #auth 에 있는 기능 모두 들고오기 - 비밀번호 변경을 위한 토큰 생성 및 확인, 캐시 남기지 않는 것 까지 전부 들어감.
from django.contrib.auth.tokens import default_token_generator #비밀번호 재설정 토큰은 기존 장고꺼 들고옴
#
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
#
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError

from django.core.validators import validate_email

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.http import JsonResponse,HttpResponse, HttpResponseRedirect

from .token import account_activation_token #인증 토큰
from .emailtext import message

from django.template.loader import render_to_string
from django.core.paginator import Paginator
#비밀번호 변경 관련 토큰 생성
UserModel = get_user_model()
INTERNAL_RESET_URL_TOKEN = 'set-password'
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'





def sign_up(request):
    context = dict()
    categories = Category.objects.all()
    context['categories'] = categories
    if request.method == "POST":
        signup_form = SignUpForm(request.POST)
        
       
        
        if signup_form.is_valid():
            
            user = CommunityUser.objects.create_user(
                nickname = request.POST["nickname"],
                email = request.POST["email"],
                password= request.POST["password1"],

            )
           
            
            user.is_active = False
            user.save()

            current_site = get_current_site(request)

            message = render_to_string('registration/user_active_email.html',{
                'user' : user,
                'domain': current_site.domain,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                'token' : account_activation_token.make_token(user),

            })

            mail_subject ="[커뮤니티 이름] 회원가입 인증 메일입니다."
            user_email = user.email
            email = EmailMessage(mail_subject, message, to=[user_email])
            email.send()

            return HttpResponse(
                  '<div style="font-size: 35px; width: 100%; height:100%; display:flex; flex-direction:column; text-align:center; '
                    'justify-content: center; align-items: center;">'
                    '<span>입력하신 이메일로 인증 링크가 전송되었습니다.</span>'
                    '<span>3분 내로 메일이 오지 않는다면 회원가입 절차를 다시 진행해주세요.</span>'
                    '</div>'
            )

            return redirect('main:index')
    else:
        signup_form = SignUpForm()
    
    context['signup_form'] = signup_form
    return render(request, 'registration/sign_up.html',context)



def activate(request, uidb64, token):

    uid = force_text(urlsafe_base64_decode(uidb64))
    user = CommunityUser.objects.get(pk=uid)

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect('success_signup')
    else:
        return HttpResponse('<div style="font-size: 40px; width: 100%; height:100%; display:flex; text-align:center; '
                'justify-content: center; align-items: center;">'
                '비정상적인 접근입니다.<span>다시 실행해주세요.</span>'
                '</div>')


#context data 가져올 수 있는 장고 클래스뷰/회원가입 입력 완료 뷰
class SuccessSignUpView(TemplateView):
    template_name = 'registration/success_signup.html'



#로그인 뷰
class LoginView(LoginView):

    template_name = 'registration/login.html'
    form_class = LoginForm
    authentication_form = LoginForm

    def get_success_url(self):
        return resolve_url(settings.LOGIN_REDIRECT_URL) #settings 에 있는 해당 url (index 페이지) 로 넘어가기

    def form_invalid(self, form):
        messages.error(self.request, '로그인에 실패했습니다. 아이디 또는 비밀번호를 확인해 주세요.', extra_tags='danger')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        
        context['categories'] = Category.objects.all()
       
        return context



#비밀번호 재설정 뷰
class MyPasswordResetView(PasswordResetView):
    success_url=reverse_lazy('login')
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    form_class = MyPasswordResetForm
    
    def form_valid(self, form):
        messages.info(self.request, '암호 변경 메일을 발송했습니다. 메일을 확인해주세요.')
        return super().form_valid(form)
   
    def form_invalid(self, form):
        messages.error(self.request, '잘못된 이메일 입니다.', extra_tags='danger')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super(MyPasswordResetView, self).get_context_data(**kwargs)
        
        context['categories'] = Category.objects.all()
       
        return context


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    success_url=reverse_lazy('login')
    template_name = 'registration/password_reset_confirm.html'
    form_class = NewPasswordSetForm
    
    def form_valid(self, form):
        messages.info(self.request, '비밀번호 변경 완료. 로그인 해주세요!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(MyPasswordResetConfirmView, self).get_context_data(**kwargs)
        
        context['categories'] = Category.objects.all()
       
        return context












@login_required
def mypage(request,pk):
    context = dict()

    user = request.user
    context['user'] = user

    user_id = CommunityUser.objects.get(pk=pk)
    context['user_id'] = user_id

    mini_categories = Mini_Category.objects.all()
    context['mini_categories'] = mini_categories
    
    categories = Category.objects.all()
    context['categories'] = categories
    
    return render(request,'mypage/mypage.html',context)

@login_required
def update_nickname(request,pk):
    context = dict()
    categories = Category.objects.all()   
    context['categories'] = categories    
    user = CommunityUser.objects.all()
    my_user = CommunityUser.objects.get(pk=pk)
    nickname_update_form = NicknameUpdateForm(instance=my_user)
    context['nickname_update_form'] = nickname_update_form

   
    if request.method == "POST":
        nickname_update_form = NicknameUpdateForm(request.POST,instance=my_user)
        
        
        if nickname_update_form.is_valid():
            save_form = nickname_update_form.save(commit=False)
            for i in user:
                
                if save_form.nickname == i.nickname:
                    messages.error(request,'닉네임이 중복됩니다! 다른 닉네임을 사용해주세요!')
                    return redirect('update_nickname',pk)

            if len(save_form.nickname)<2 or len(save_form.nickname)>8:
                messages.error(request,'닉네임은 2자 이상 8자 이하입니다.')
                return redirect('update_nickname',pk)


            nickname_update_form.save()
            #여기서는 url 요청이 아니라서 렌더 
            return render(request,'mypage/update_nickname_complete.html',context)
        
      
    return render(request,'mypage/update_nickname.html',context) 


@login_required
def my_post(request):
    context = dict()
    my_user = request.user
    user = my_user.nickname
    my_post = Post.objects.filter(writer=user)
    context['my_post'] = my_post
    
    paginator = Paginator(my_post, 10)
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number) 
    context['page_obj'] = page_obj

    context['categories'] = Category.objects.all()
    return render(request,'mypage/my_post.html',context)

@login_required
def my_like(request):
    context = dict()
    user = request.user
    likes = user.like_post.all()
    
    paginator = Paginator(likes, 10)
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number) 
    context['page_obj'] = page_obj
    context['likes'] = likes

    context['categories'] = Category.objects.all()
    return render(request,'mypage/my_like.html',context)


