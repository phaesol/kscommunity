from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Mini_Category(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category,on_delete=models.CASCADE , related_name="mini_category") 
    
    def __str__(self):
        return self.title
        
class Post(models.Model):
    writer = models.CharField(max_length=10)
    title = models.CharField(max_length=50)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now_add= True) # 최초 생성 날짜만 갱신
    myimage = models.ImageField(null = True, blank = True)
    category = models.ForeignKey(Mini_Category,on_delete=models.CASCADE) 

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE) 
    body = models.CharField('댓글 작성하기',max_length=150)  #'댓글 작성하기'을 준 이유는 나중에 label이름을 body가 아닌 댓글 작성하기로 바꾸기 위해서.
    created_at = models.DateTimeField(auto_now_add=True)    # 수정은 하지 않고, 삭제만 주기


    def __str__(self):        
        return self.body


class ReComment(models.Model):
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name="recomment")
    body = models.CharField('',max_length=150) #대댓글은 이름일단 없앰.
    created_at = models.DateTimeField(auto_now_add=True)
