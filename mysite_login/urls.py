# mysite_login/urls.py

from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from login import views
from login.views import ForgetPwdView,RestpwdView,ModifypwdView
from django.urls import re_path

urlpatterns = [

 path('login/', views.login,name='login'),
 path('', include('captcha.urls')),

 path('register/', views.register,name='register'),
 path('', views.index),
 path('admin/', admin.site.urls),

 path('forgetpwd/', ForgetPwdView.as_view(), name='forgetpwd'),  # 忘记密码
 re_path('forgetpwd/reset/(?P<active_code>.*)/', RestpwdView.as_view(), name='resetpwd'),  # 密码重置验证
 path('modify_pwd/', ModifypwdView.as_view(), name="modify_pwd"),  # 密码修改
]
