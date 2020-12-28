from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin, HitCount

class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Mini_Category(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category,on_delete=models.CASCADE , related_name="mini_category") 
    
    def __str__(self):
        return self.title
        
class Post(models.Model, HitCountMixin):
    writer = models.CharField(max_length=8)
    title = models.CharField(max_length=50)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now_add= True) # 최초 생성 날짜만 갱신
    myimage = models.ImageField(null = True, blank = True)
    category = models.ForeignKey(Mini_Category,on_delete=models.CASCADE) 
    like_count = models.PositiveIntegerField(default=0)
    # GenericRelatio로 조회수별로 정렬할수 있음
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )
    
    def __str__(self):
        return self.title

    def current_hit_count(self):
        return self.hit_count.hits

class Comment(models.Model):
    writer = models.CharField(max_length=8)
    post = models.ForeignKey(Post,on_delete=models.CASCADE) 
    body = models.CharField('댓글 작성하기',max_length=150)  #'댓글 작성하기'을 준 이유는 나중에 label이름을 body가 아닌 댓글 작성하기로 바꾸기 위해서.
    created_at = models.DateTimeField(auto_now_add=True)    # 수정은 하지 않고, 삭제만 주기


    def __str__(self):        
        return self.body


class ReComment(models.Model):
    writer = models.CharField(max_length=8)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name="recomment")
    body = models.CharField('',max_length=150) #대댓글은 이름일단 없앰.
    created_at = models.DateTimeField(auto_now_add=True)

