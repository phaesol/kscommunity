from django import forms
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth import password_validation, update_session_auth_hash
from .models import CommunityUser,UserManager
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    # 회원가입 기본 폼에 있는 패스워드, 패스워드 확인 상속
    
    class Meta:
        model = CommunityUser
        fields = ['nickname', 'email','password1','password2',]

    def clean(self):
        #cleaned_data : 유효성 검사를 마친 후 딕셔너리 타입으로 정의 - 뒤에 get 을 붙이면 키 값 불확실 하지 않을 때 사용.
        #cleaned_data : 키에러 / cleaned_data.get() : None 반환
        nickname = self.cleaned_data.get('nickname')
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
      
        if CommunityUser.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError('이미 존재하는 닉네임입니다.')
        

        if password1!=password2:
            raise forms.ValidationError('비밀번호가 서로 일치하지 않습니다. 다시 입력해주세요.')
        
         
        try:
            CommunityUser.objects.get(email=email)
            raise forms.ValidationError('이미 존재하는 이메일입니다.')
        except CommunityUser.DoesNotExist:
            pass
        #잘못입력했을 경우
        if email is None:
            raise forms.ValidationError('올바른 이메일을 입력해주세요.')
        #경성대 이메일이 아닌 경우, split 사용 @ 기준으로 나눠서 리스트 형태
        if email.split('@')[1] != 'ks.ac.kr':
            raise forms.ValidationError('경성대 이메일을 입력해주세요!')
        
        
        #비밀번호 설정
        try:
            password_validation.validate_password(password1,self.instance)
        except forms.ValidationError:
            raise forms.ValidationError('8자 이상의 안전한 비밀번호로 설정해주세요.')
        if password1 != password2:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
       
        if len(nickname)==1 or len(nickname)>=8:
            raise forms.ValidationError('닉네임은 2자 이상, 8자 이하입니다.')
        #닉네임 중복 확인
        try:
            CommunityUser.objects.get(nickname=nickname)
            raise forms.ValidationError("이미 존재하는 닉네임입니다.")
        except CommunityUser.DoesNotExist:
            pass
        return self.cleaned_data
    


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': '로그인에 실패했습니다. 아이디 또는 비밀번호를 확인해 주세요.',
        'inactive': "로그인에 실패했습니다. 아이디 또는 비밀번호를 확인해 주세요.",
    }
    
    def __init__(self,*args,**kwargs):
        super(LoginForm,self).__init__(*args,**kwargs)

        UserModel = CommunityUser
        



class NicknameUpdateForm(forms.ModelForm):
    class Meta:
        model = CommunityUser
        fields = ['nickname',]
    
    
        


# class PasswordUpdateForm(PasswordChangeForm):

#     old_password = forms.CharField(
#         label='기존 비밀번호',
#         strip=False,
#         widget=forms.PasswordInput(
#             attrs={
#                 'autocomplete': 'current-password', 
#                 'autofocus': True} ),
#     )

#     new_password1 = forms.CharField(
#         label='새 비밀번호',
#         strip=False,
#         widget=forms.PasswordInput(
#             attrs={'autocomplete': 'new-password' }),
#         help_text=password_validation.password_validators_help_text_html(),
#     )
#     new_password2 = forms.CharField(
#         label='새 비밀번호 확인',
#         strip=False,
#         widget=forms.PasswordInput(
#             attrs={'autocomplete': 'new-password'}),
#     )


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label = '이메일',
        max_length=100,
        widget=forms.EmailInput(
            attrs={'autocomplete': 'email'}),
    )
    
    def clean(self):
        email = self.cleaned_data.get('email')
        if email is None:
            raise forms.ValidationError('올바른 이메일을 입력해주세요.')
        if email.split('@')[1] != 'ks.ac.kr':
            raise forms.ValidationError('경성대 이메일을 입력해주세요!')
        try:
            CommunityUser.objects.get(email=email)
            pass
        except CommunityUser.DoesNotExist:
            raise forms.ValidationError('해당 이메일이 없습니다. 다시 확인해주세요.')

class NewPasswordSetForm(SetPasswordForm):
  
    error_messages = {
        'password_mismatch': '두 비밀번호가 서로 일치하지 않습니다.',
    }
    new_password1 = forms.CharField(
        label="새 비밀번호",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="새 비밀번호 확인",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

   

    
    