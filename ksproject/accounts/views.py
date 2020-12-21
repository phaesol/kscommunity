# import jwt
import json


from django.shortcuts import render,redirect
from django.conf import settings
from django.urls import reverse_lazy
from django.shortcuts import resolve_url, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site


from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView

from .forms import SignUpForm, LoginForm, NicknameUpdateForm, PasswordUpdateForm,PasswordResetForm,NewPasswordSetForm
from .models import CommunityUser
from board.models import Post,Mini_Category,Category

from django.contrib.auth.views import LoginView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import auth,messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
) #auth 에 있는 기능 모두 들고오기 - 비밀번호 변경을 위한 토큰 생성 및 확인, 캐시 남기지 않는 것 까지 전부 들어감.
from django.contrib.auth.tokens import default_token_generator #비밀번호 재설정 토큰은 기존 장고꺼 들고옴


from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError

from django.core.validators import validate_email

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.http import JsonResponse,HttpResponse, HttpResponseRedirect

from .token import account_activation_token #인증 토큰
from .emailtext import message

#비밀번호 변경 관련 토큰 생성
UserModel = get_user_model()
INTERNAL_RESET_URL_TOKEN = 'set-password'
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'


# class SignUpView(CreateView):
#     model = get_user_model()
#     form_class = SignUpForm
#     success_url = '/user/login/'
#     verify_url = '/user/verify/'
#     token_generator = default_token_generator

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         if form.instance:
#             self.send_verification_email(form.instance)
#         return response

#     def send_verification_email(self, user):
#         token = self.token_generator.make_token(user)
#         user.email_user('회원가입을 축하드립니다.', '다음 주소로 이동하셔서 인증하세요. {}'.format(self.build_verification_link(user, token)), from_email=settings.EMAIL_HOST_USER)
#         messages.info(self.request, '회원가입을 축하드립니다. 가입하신 이메일주소로 인증메일을 발송했으니 확인 후 인증해주세요.')

#     def build_verification_link(self, user, token):
#         return '{}/user/{}/verify/{}/'.format(self.request.META.get('HTTP_ORIGIN'), user.pk, token)

# class UserVerificationView(TemplateView):

#     model = get_user_model()
#     redirect_url = '/user/login/'
#     token_generator = default_token_generator

#     def get(self, request, *args, **kwargs):
#         if self.is_valid_token(**kwargs):
#             messages.info(request, '인증이 완료되었습니다.')
#         else:
#             messages.error(request, '인증이 실패되었습니다.')
#         return HttpResponseRedirect(self.redirect_url)   # 인증 성공여부와 상관없이 무조건 로그인 페이지로 이동

#     def is_valid_token(self, **kwargs):
#         pk = kwargs.get('pk')
#         token = kwargs.get('tonen')
#         user = self.model.objects.get(pk=pk)
#         is_valid = self.token_generator.check_token(user, token)
#         if is_valid:
#             user.is_active = True
#             user.save()     # 데이터가 변경되면 반드시 save() 메소드 호출
#         return is_valid


#회원가입 뷰
# class SignUpView(CreateView):
#     template_name = 'registration/sign_up.html'
#     form_class = SignUpForm
#     # user = None

#     def get_success_url(self,**kwargs):
        
#         #인증 이메일 보내는 함수
#         domain = "http://127.0.0.1:8000/" #나중에 변경
#         uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk)) #url 인코딩 방법
#         token = account_activation_token.make_token(self.user) # token 생성 함수 불러오기
#         message_data = message(domain, uidb64, token) #emailtext.py 에 있는 message에 각 변수 대입해서 message_date 변수 생성
#         #장고 이메일 보내는 기능 - 커뮤니티 이름 추후에 수정/제목 서브젝트,일반텍스트 바디,수신자주소 to 기입
#         email = EmailMessage(
#             '(커뮤니티 이름) 인증 메일 요청입니다.',
#             message(domain,uidb64,token),
#             to=[self.user.email]
#         )

#         email.send()

#         return reverse_lazy('success_signup')


#         def form_valid(self, form):
#             self.user = form.save()  # 폼 save 메소드에서 return user 저장
#             return super().form_valid(form)
#         #경성대 이메일이 아니거나, 잘못된 이메일 형식
#         def form_invalid(self, form):
#             message.error(self.request, form.non_field_errors(),extra_tags='danger')
#             return super().form_invalid(form)

# class SignUpView(CreateView):
#     template_name = 'registration/sign_up.html'
#     form_class = SignUpForm
   

#     def post(self,request):
        
#         data = json.loads(request.body.decode("utf-8"))
        
#         try:
#             validate_email(data["email"])

#             if CommunityUser.objects.filter(email=data["email"]).exists():
#                 return JsonResponse({"message" : "EXISTS_EMAIL"},status=400)

#             user = CommunityUser.objects.create(
#                 email = data["email"],
#                 password = bcrypt.hashpw(data["password"].encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8"),
#                 is_active = False
#             )

#             domain = "http://127.0.0.1:8000/" #나중에 변경
#             uidb64 = urlsafe_base64_encode(force_bytes(user.pk)) #url 인코딩 방법
#             token = account_activation_token.make_token(user) # token 생성 함수 불러오기
#             message_data = message(domain, uidb64, token) #emailtext.py 에 있는 message에 각 변수 대입해서 message_date 변수 생성

#             maile_title = "(커뮤니티 이름) 인증 메일입니다. "
#             mail_to = data['email']
#             email = EmailMessage(maile_title,message_data,to=[mail_to])
#             email.send()
 
#             return JsonResponse({"message" : "SUCCESS"}, status=200)
        
#         except KeyError:
#             return JsonResponse({"message" : "INVALED_KEY"}, status=400)

         
#         except TypeError:
#             return JsonResponse({"message" : "INVALED_TYPE"}, status=400)

         
#         except ValidationError:
#             return JsonResponse({"message" : "VALIDATION_ERROR"}, status=400)

class SignUpView(CreateView):
    template_name = 'registration/sign_up.html'
    form_class = SignUpForm
    # user = None

    # def signup(request):
    #     if request.method == "POST":
    #         if request.POST["password1"] == request.POST["password2"]:
    #             user = CommunityUser.objects.create_user(
    #                 username=request.POST["username"],
    #                 password=request.POST["password1"],
    #                 nickname = request.POST["nickname"])
    #             user.is_active = False
    #             user.save()
         
    #             current_site = get_current_site(request) 
    #             # localhost:8000
    #             message = render_to_string('accounts/user_activate_email.html',                         {
    #                 'user': user,
    #                 'domain': current_site.domain,
    #                 'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
    #                 'token': account_activation_token.make_token(user),
    #             })  
    #             mail_subject = "[SOT] 회원가입 인증 메일입니다."
    #             user_email = user.username
    #             email = EmailMessage(mail_subject, message, to=[user_email])
    #             email.send()
    #             return HttpResponse(
    #                 '<div style="font-size: 40px; width: 100%; height:100%; display:flex; text-align:center; '
    #                 'justify-content: center; align-items: center;">'
    #                 '입력하신 이메일<span>로 인증 링크가 전송되었습니다.</span>'
    #                 '</div>'
    #             )
    #             return redirect('main:index')
    #     return render(request, 'accounts/sign_up.html')     
               

    # def form_valid(self, form):
    #     self.user = form.save()  # 폼 save 메소드에서 return user 저장
    #     return super().form_valid(form)
    # #경성대 이메일이 아니거나, 잘못된 이메일 형식
    # def form_invalid(self, form):
    #     message.error(self.request, form.non_field_errors(),extra_tags='danger')
    #     return super().form_invalid(form)


def activate(request, uid64, token):

    uid = force_text(urlsafe_base64_decode(uid64))
    user = CommunityUser.objects.get(pk=uid)

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect('main:index')
    else:
        return HttpResponse('비정상적인 접근입니다.')


#context data 가져올 수 있는 장고 클래스뷰/회원가입 입력 완료 뷰
class SuccessSignUpView(TemplateView):
    template_name = 'registration/success_signup.html'



#이메일 인증 처리 뷰
class ActivateView(TemplateView):
    template_name = 'registration/activate.html'

    def get(self,request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64)) # 위 uidb64 디코딩
            user = CommunityUser.objects.get(pk=uid) #user pk=uid 확인

            if account_activation_token.check_token(user,token):
                user.is_active = True
                user.save()
                auth.login(request,user)

                return super(ActivateView,self).get(request,uid64, token)

            return JsonResponse({"message":"AUTH_FAIL"}, status=400 ) # 다르면 에러 띄워주기
                   #JsonResponse: response 를 메세지와 status code를 함께 보내줄 수 있음. 프론트개발자와 규칙 정의 - 보통 내용은 자세히 적지말고, 띄워쓰기 불포함, 벨류값은 대문자로.
        
        except ValidationError:
            return JsonResponse({"message": "TYPE_ERROR"}, status=400)

        except KeyError:
            return JsonResponse({"message":"INVALID_KEY"}, status=400)

#로그인 뷰
class LoginView(LoginView):

    template_name = 'registration/login.html'
    form_class = LoginForm
    authentication_form = LoginForm

    def get_success_url(self):
        return resolve_url(settings.LOGIN_REDIRECT_URL) #settings 에 있는 해당 url (index 페이지) 로 넘어가기

    def form_invalid(self, form):
        # messages.error(self.request, '로그인에 실패했습니다. 아이디 또는 비밀번호를 확인해 주세요.', extra_tags='danger')
        return super().form_invalid(form)


# #class 형 뷰에서는 데코레이터를 이렇게 쓴다.
# @method_decorator(login_required, name='dispatch')
# #마이페이지 업데이트 뷰 / templateview 형식
# class UpdateMyPageView(TemplateView):

#     template_name = 'mypage/update_mypage.html'
    
#     def get_context_data(self, **kwargs):

#         context = super(UpdateMyPageView, self).get_context_data(**kwargs)

#         context['nickname_form'] = NicknameUpdateForm(
#             instance= self.request.user,
#             prefix = 'nickname_form', #접두사 사용
#             data = self.request.POST if 'nickname_form-submit' in self.request.POST else None,
#         )


#         context['password_form'] = PasswordUpdateForm(
#             user= self.request.user,
#             prefix = 'password_form', #접두사 사용
#             data = self.request.POST if 'password_form-submit' in self.request.POST else None,
#         )


#         return context

#     def post(self, request, *args, **kwargs):

#         context = self.get_context_data(**kwargs)

#         if context['nickname_form'].is_valid():
#             context['nickname_form'].save()
#             messages.success(request,'닉네임 변경 완료')

#         elif context['password_form'].is_valid():
#             context['password_form'].save()
#             messages.success(request,'비밀번호 변경 완료')

#         else:
#             messages.error(self.request,'저장되지 않았습니다. 다시 확인해주세요.')

#         return self.render_to_response(context)







class UserPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html'
    success_url = reverse_lazy('password_reset_done')
    form_class = PasswordResetForm

    #폼 유효성 검사
    def form_valid(self,form):
        #이메일이 요청한 유저와 같으면, 검사 통과 
        if CommunityUser.objects.filter(email=self.request.POST.get('email')).exists():
            return super().form_valid(form)
        #이메일 유효하지 않으면, fail html 띄워줌.
        else:
            return render(self.request,'password_reset_done_fail.html')
    
  





class UserPasswordResetDoneView(PasswordResetDoneView):
    #template_name 은 같아서 굳이 안적어줘도 됨.
    template_name = 'registration/password_reset_done.html'
    title = '비밀번호 재설정 발송 '


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    success_url=reverse_lazy('password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'
    form_class = NewPasswordSetForm
    
    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '새 비밀번호 생성에 실패했습니다. 다시 시도해주세요. ', extra_tags='danger')
        return super().form_invalid(form)


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registraion/password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
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
        update_form = NicknameUpdateForm(request.POST,instance=my_user)
        
        
        if update_form.is_valid():
            save_form = update_form.save(commit=False)
            for i in user:
                
                if save_form.nickname == i.nickname:
                    messages.error(request,'닉네임이 중복됩니다! 다른 닉네임을 사용해주세요!')
                    return redirect('update_nickname',pk)

            if len(save_form.nickname)<2 or len(save_form.nickname)>8:
                messages.error(request,'닉네임은 2자 이상 8자 이하입니다.')
                return redirect('update_nickname',pk)


            update_form.save()
            #여기서는 url 요청이 아니라서 렌더 
            return render(request,'mypage/update_nickname_complete.html',context)
        
      
    return render(request,'mypage/update_nickname.html',context) 




