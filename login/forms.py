from django import forms
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')

class RegisterForm(forms.Form):
 gender = (
  ('male', "男"),
  ('female', "女"),
 )
 username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
 password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
 password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
 email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
 sex = forms.ChoiceField(label='性别', choices=gender)
 captcha = CaptchaField(label='验证码')


# 找回密码form实现
class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


# 重置密码form实现
class ModifyPwdForm(forms.Form):
    # 密码不能小于5位
    password1 = forms.CharField(required=True, min_length=5)
    # 密码不能小于5位
    password2 = forms.CharField(required=True, min_length=5)

