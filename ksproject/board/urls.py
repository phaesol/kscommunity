from django.contrib import admin 
from django.urls import path 
from .views import free,free_create,private,private_create,free_detail,create_comment,free_update,free_delete,search



urlpatterns = [
  path('free/',free,name="free"),
  path('free_create',free_create, name="free_create"),
  path('private/',private, name="private"),
  path('private/create/',private_create, name="private_create"),
  path('free/detail/<int:post_id>',free_detail,name="free_detail"),
  path('free/update/<int:post_id>',free_update,name="free_update"),
  path('free/delete/<int:post_id>',free_delete,name="free_delete"),  
  path('create_comment/<int:post_id>',create_comment,name="create_comment"), 
  path('search',search,name="search"),
  # path('private/update/<int:pk>',PrivateUpdate.as_view(),name="private_update"), 

]