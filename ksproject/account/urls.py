from django.contrib import admin 
from django.urls import path ,include

from django.contrib.auth.views import LogoutView
from account.views import SignUpView,SuccessSignUpView, ActivateView, LoginView, UpdateMyPageView,UserPasswordResetView,UserPasswordResetDoneView,UserPasswordResetConfirmView,UserPasswordResetCompleteView,mypage



urlpatterns = [
  path('signup/', SignUpView.as_view(), name='signup'),
  path('success_signup/', SuccessSignUpView.as_view(), name='success_signup'),
  path('account/activate/<str:uidb64>/<str:token>/',ActivateView.as_view(), name='activate'),
  path('login/', LoginView.as_view(), name='login'),
  path('logout/',LogoutView.as_view(),name="logout"),
  path('mypage/',mypage,name="mypage"),
  path('mypage/<int:pk>/update_mypage',UpdateMyPageView.as_view(),name="update_mypage"),
  path('password_reset/',UserPasswordResetView.as_view(),name="password_reset"),
  path('password_reset_done/', UserPasswordResetDoneView.as_view(), name="password_reset_done"),
  path('password_reset_confirm/<str:uidb64>/<str:token>/', UserPasswordResetConfirmView.as_view(), name="password_reset_confrim"),
  path('password_reset_complete/', UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),
  ]