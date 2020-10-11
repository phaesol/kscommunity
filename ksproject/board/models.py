from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now = True)
    myimage = models.ImageField(null = True, blank = True)
    category = models.CharField(max_length=50,default="") 



class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE) #Post의 게시물이 삭제되면, 그 게시물에 있던 댓글도 삭제되는 on_delete 옵션
    body = models.CharField('댓글 작성하기',max_length=150)          #'댓글 작성하기'을 준 이유는 나중에 label이름을 body가 아닌 댓글 작성하기로 바꾸기 위해서.
    created_at = models.DateTimeField(auto_now=True)        #현재 시간 자동 생성


    def __str__(self):         #모델 클래스의 객체의 문자열 표현을 리턴한다.
        return self.body
