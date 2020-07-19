"""
author: taosiliang
create: time: 2020-07-09
update：time: 2020-07-11
"""


# login/views.py

from django.shortcuts import render,reverse, redirect
from . import models
from .forms import UserForm
from .forms import RegisterForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
import random
from django.contrib.auth.hashers import make_password
import re
from random import Random
from django.views.generic import View


def index(request):
    pass
    return render(request, 'login/index.html')


def login(request):
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/index.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = make_password(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    pass
    return redirect('/index/')



from django.core.mail import send_mail
from login.models import EmailVerifyRecord
from mysite_login.settings import EMAIL_FROM


from .forms import RegisterForm, ForgetPwdForm, ModifyPwdForm
from captcha.fields import CaptchaStore
from captcha.helpers import captcha_image_url
from login.email_send import send_register_email

# 忘记密码视图
class ForgetPwdView(View):
    def get(self, request):
        forgetpwd_form = ForgetPwdForm()
        # 图片验证码
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        return render(request, 'login/forgetpwd.html',
                      {
                          'forgetpwd_form': forgetpwd_form,
                          'hashkey': hashkey,
                          'image_url': image_url,
                      })

    def post(self, request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        # 图片验证码
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)

        if forgetpwd_form.is_valid():
            email = request.POST.get('email', '')
            if models.User.objects.filter(email=email):
                # 如果邮箱是注册过的，就发送改密邮件，然后跳回登录页面
                send_register_email(request_uri=request.build_absolute_uri(), email=email, send_type='forget')

                return render(request, 'login/login.html',
                              {
                                  'msg': '重置密码邮件已发送,请注意查收',
                              })
            else:
                return render(request, 'login/forgetpwd.html',
                              {
                                  'forgetpwd_form': forgetpwd_form,
                                  'hashkey': hashkey,
                                  'image_url': image_url,
                                  'msg': '邮箱未注册，请检查是否输入错误'
                              })
        else:
            return render(request, 'login/forgetpwd.html',
                          {
                              'forgetpwd_form': forgetpwd_form,
                              'hashkey': hashkey,
                              'image_url': image_url,
                          })



# 重置密码
class RestpwdView(View):
    def get(self, request, active_code):
        # 查询验证码是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)

        if all_record:
            for record in all_record:
                email = record.email

                return render(request, 'login/pwdreset.html',
                              {
                                  'email': email
                              })
        else:
            forgetpwd_form = ForgetPwdForm()
            hashkey = CaptchaStore.generate_key()
            image_url = captcha_image_url(hashkey)

            return render(request, 'login/forgetpwd.html',
                          {
                              'forgetpwd_form': forgetpwd_form,
                              "msg": "您的重置链接无效",
                              'hashkey': hashkey,
                              'image_url': image_url,
                          })


# 修改密码
class ModifypwdView(View):
    def post(self, request):
        modifypwd_form = ModifyPwdForm(request.POST)

        if modifypwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            # 如果两次密码不相等，返回错误信息
            if pwd1 != pwd2:
                return render(request, "login/pwdreset.html",
                              {
                                  "email": email,
                                  "msg": "密码不一致",
                                  'modifypwd_form': modifypwd_form,
                               })
            # 如果密码一致
            user = models.User.objects.get(email=email)
            # 加密成密文
            user.password = make_password(pwd2)
            # save保存到数据库
            user.save()
            return render(request, "login/login.html", {"msg": "密码修改成功，请登录"})
        else:
            email = request.POST.get("email", "")
            return render(request, 'login/pwdreset.html',
                          {
                             'email': email,
                             'modifypwd_form': modifypwd_form,
                          })
