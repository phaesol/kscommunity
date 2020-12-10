from django.shortcuts import render,redirect
from django.conf import settings
from django.urls import reverse_lazy
from django.shortcuts import resolve_url, get_object_or_404

from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView

from .forms import SignUpForm, LoginForm, NicknameUpdateForm, PasswordUpdateForm,PasswordResetForm,NewPasswordSetForm
from .models import CommunityUser
from board.models import Post,Mini_Category

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

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.http import JsonResponse,HttpResponse, HttpResponseRedirect

from .token import account_activation_token #인증 토큰
from .emailtext import message

#비밀번호 변경 관련 토큰 생성
UserModel = get_user_model()
INTERNAL_RESET_URL_TOKEN = 'set-password'
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'



#회원가입 뷰
class SignUpView(CreateView):
    template_name = 'registration/sign_up.html'
    form_class = SignUpForm
    user = None

    def get_success_url(self):
        #인증 이메일 보내는 함수
        domain = "http://127.0.0.1:8000/" #나중에 변경
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk)) #url 인코딩 방법
        token = account_activation_token.make_token(self.user) # token 생성 함수 불러오기
        message_data = message(domain, uidb64, token) #emailtext.py 에 있는 message에 각 변수 대입해서 message_date 변수 생성
        #장고 이메일 보내는 기능 - 커뮤니티 이름 추후에 수정/제목 서브젝트,일반텍스트 바디,수신자주소 to 기입
        email = EmailMessage(
            '(커뮤니티 이름) 인증 메일 요청입니다.',
            message(domain,uidb64,token),
            to=[self.user.email]
        )

        email.send()

        return reverse_lazy('success_signup')


        def form_valid(self, form):
            self.user = form.save()  # 폼 save 메소드에서 return user 저장
            return super().form_valid(form)
        #경성대 이메일이 아니거나, 잘못된 이메일 형식
        def form_invalid(self, form):
            message.error(self.request, form.non_field_errors(),extra_tags='danger')
            return super().form_invalid(form)



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
        messages.error(self.request, '로그인에 실패했습니다. 아이디 또는 비밀번호를 확인해 주세요.', extra_tags='danger')
        return super().form_invalid(form)


#class 형 뷰에서는 데코레이터를 이렇게 쓴다.
@method_decorator(login_required, name='dispatch')
#마이페이지 업데이트 뷰 / templateview 형식
class UpdateMyPageView(TemplateView):

    template_name = 'mypage/update_mypage.html'
    
    def get_context_data(self, **kwargs):

        context = super(UpdateMyPageView, self).get_context_data(**kwargs)

        context['nickname_form'] = NicknameUpdateForm(
            instance= self.request.user,
            prefix = 'nickname_form', #접두사 사용
            data = self.request.POST if 'nickname_form-submit' in self.request.POST else None,
        )


        context['password_form'] = PasswordUpdateForm(
            user= self.request.user,
            prefix = 'password_form', #접두사 사용
            data = self.request.POST if 'password_form-submit' in self.request.POST else None,
        )


        return context

    def post(self, request, *args, **kwargs):

        context = self.get_context_data(**kwargs)

        if context['nickname_form'].is_valid():
            context['nickname_form'].save()
            messages.success(request,'닉네임 변경 완료')

        elif context['password_form'].is_valid():
            context['password_form'].save()
            messages.success(request,'비밀번호 변경 완료')

        else:
            messages.error(self.request,'저장되지 않았습니다. 다시 확인해주세요.')

        return self.render_to_response(context)





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



def mypage(request):
    context = dict()
    mini_categories = Mini_category.objects.all()
    context['mini_categories'] = mini_categories
    return render(request,'mypage/mypage.html',context)



