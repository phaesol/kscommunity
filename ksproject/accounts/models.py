from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db import models 
from django.core.exceptions import ValidationError
from board.models import Post

class UserManager(BaseUserManager):    
    
    use_in_migrations = True    
    


    def create_user(self, email, nickname, password=None):        
        #유저 생성 시 실행되는 함수
        if not email :            
            raise ValueError('이메일은 필수입니다!')        
      
        user = self.model(
        #이메일 입력시 대소문자 구분 없기 위함.            
        email = self.normalize_email(email),            
        nickname = nickname,     
        ) 

        user.is_admin = False      
        user.is_superuser = False      
        user.is_staff = False
        user.is_active = True     
        

        #비밀번호에 해시값으로 저장 후 해시값과 기존 값 비교하여 보안 동시에 입력값과 비교.       
        user.set_password(password)        
        user.save(using=self._db)   

        return user      

   



    def create_superuser(self, email, nickname,password ):        
        #슈퍼유저 생성
        user = self.create_user(            
            email = self.normalize_email(email),            
            nickname = nickname,            
            password=password        
        )        
        user.is_admin = True        
        user.is_superuser = True        
        user.is_staff = True        
        user.is_active = True
        
        user.save(using=self._db)        
        return user 


#PermissionsMixin - : 기본 그룹, 허가권 관리 기능 재사용
class CommunityUser(AbstractBaseUser,PermissionsMixin):    
    #헬퍼 클래스 지정
    
    objects = UserManager()

   
    
    email = models.EmailField(        
        max_length=100,
        null=False,      
        unique=True,
        verbose_name="이메일"   
    )
        
    nickname = models.CharField(
        max_length=10,
        null=False,
        unique=True,
        verbose_name="닉네임"
    )   
    
    likes = models.ManyToManyField(to=Post, related_name='likers')
      
    is_active = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)    
    is_superuser = models.BooleanField(default=False)    
    is_staff = models.BooleanField(default=False)     
    
    #last_login 은 업뎃할 때 마다 시간 업뎃.
    date_joined = models.DateTimeField(verbose_name="date_joined",auto_now_add=True)     
    last_login = models.DateTimeField(verbose_name="last_login",auto_now = True)
    
    
    USERNAME_FIELD = 'email'    
    REQUIRED_FIELDS = ['nickname']

    class Meta:
        
        verbose_name = ("user")
        verbose_name_plural = ("users")
        
        
        def __str__(self):
            return self.email