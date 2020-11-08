from django.contrib import admin 
from django.urls import path 
from .views import create,post_list


urlpatterns = [
  path('create/<int:mini_category_id>',create, name="create"),
  path('post_list/<int:mini_category_id>',post_list,name="post_list"),
 
  ]