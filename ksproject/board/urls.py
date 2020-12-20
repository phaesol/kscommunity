from django.contrib import admin 
from django.urls import path 
from .views import create,post_list,detail,update_post,search,create_comment,delete_comment,create_recomment,delete_recomment


urlpatterns = [
  path('create/<int:mini_category_id>',create, name="create"),
  path('post_list/<int:mini_category_id>',post_list,name="post_list"),
  path('detail/<int:post_id>',detail,name="detail"),
  path('update_post/<int:post_id>',update_post,name="update_post"),
  path('create_comment/<int:post_id>',create_comment,name="create_comment"),
  path('delete_comment/<int:post_id>/<int:com_id>',delete_comment,name="delete_comment"),
  path('create_recomment/<int:post_id>/<int:com_id>',create_recomment,name='create_recomment'),
  path('delete_recomment/<int:post_id>/<int:com_id>',delete_recomment,name="delete_recomment"),
  path('search',search, name="search"),
  ]