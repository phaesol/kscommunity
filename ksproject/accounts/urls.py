from django.contrib import admin 
from django.urls import path ,include

from django.contrib.auth.views import LogoutView
from accounts.views import *


urlpatterns = [
  path('signup/', sign_up, name='signup'),
  path('success_signup/', SuccessSignUpView.as_view(), name='success_signup'),
  path('activate/<str:uidb64>/<str:token>/',activate, name='activate'),
  path('login/', LoginView.as_view(), name='login'),
  path('logout/',LogoutView.as_view(),name="logout"),
  path('mypage/<int:pk>',mypage,name="mypage"),
  path('mypage/update_nickname/<int:pk>',update_nickname,name="update_nickname"),
  path('password_reset/',UserPasswordResetView.as_view(),name="password_reset"),
  path('password_reset_done/', UserPasswordResetDoneView.as_view(), name="password_reset_done"),
  path('password_reset_confirm/<str:uidb64>/<str:token>/', UserPasswordResetConfirmView.as_view(), name="password_reset_confrim"),
  path('password_reset_complete/', UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),
  ]