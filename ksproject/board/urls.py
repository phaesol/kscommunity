from django.contrib import admin 
from django.urls import path 
from .views import *


urlpatterns = [
  path('create/<int:mini_category_id>',create, name="create"),
  path('post_list/<int:mini_category_id>',post_list,name="post_list"),
  path('detail/<int:pk>',PostDetail.as_view(),name="detail"),
  path('update_post/<int:post_id>',update_post,name="update_post"),
  path('delete_post/<int:pk>',deleteView.as_view(),name="delete_post"),
  path('create_comment/<int:post_id>',create_comment,name="create_comment"),
  path('delete_comment/<int:com_id>',delete_comment,name="delete_comment"),
  path('create_recomment/<int:post_id>/<int:com_id>',create_recomment,name='create_recomment'),
  path('delete_recomment/<int:recom_id>',delete_recomment,name="delete_recomment"),
  path('search/',search, name="search"),
  path('like_toggle/<int:post_id>',like_toggle,name="like_toggle")
  ]