# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import auth
from  socialnetwork.account.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30
        , label='用户名'
        , required=True
        , widget=forms.TextInput(attrs={'placeholder': u'用户名'})
        , error_messages={'required': u'用户名不能为空!'})
    password = forms.CharField(max_length=30
        , label='密码'
        , required=True
        , widget=forms.PasswordInput(attrs={'placeholder': u'密码'})
        , error_messages={'required': u'密码不能为空!'}
    )
    remember = forms.BooleanField(required=False
        , widget=forms.CheckboxInput()
    )


    def auth_user(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = auth.authenticate(username=username, password=password)
        if not user:
            msg = u'用户名或密码错误!'
            self._errors["username"] = self.error_class([msg])
            return self
        else:
            return self


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=30
        , label='用户名'
        , required=True
        , widget=forms.TextInput(attrs={'placeholder': u'用户名'})
        , error_messages={'required': u'用户名不能为空！'}
    )
    password = forms.CharField(max_length=30
        , label='密码'
        , required=True
        , widget=forms.PasswordInput(attrs={'placeholder': u'密码'})
        , error_messages={'required': u'密码不能为空！'}
    )
    password_confirm = forms.CharField(max_length=30
        , label='密码确认'
        , required=True
        , widget=forms.PasswordInput(attrs={'placeholder': u'密码确认'})
        , error_messages={'required': u'密码确认不能为空！'}
    )

    email = forms.EmailField(max_length=30
        , label='邮箱'
        , required=True
        , widget=forms.TextInput(attrs={'placeholder': u'邮箱'})
        , error_messages={'required': u'邮箱不能为空！', 'invalid': u'请输入正确的邮箱！'}
    )


    def auth_user(self):
        username = self.cleaned_data.get('username')
        is_exist = User.objects.filter(username=username)

        if is_exist:
            msg = u'用户名已存在'
            self._errors["username"] = self.error_class([msg])
            return self
        else:
            return self

    def auth_email(self):
        email = self.cleaned_data.get('email')
        is_exist = User.objects.filter(email=email)

        if is_exist:
            msg = u'邮箱已被注册'
            self._errors["email"] = self.error_class([msg])
            return self
        else:
            return self


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user','avatar_little','avatar_middle','shorturl')
        widgets = {
            'gender': forms.RadioSelect(attrs={'class': 'radio inline'}),
            'birthday': forms.TextInput(attrs={'class': "Wdate id_location",
                                               'id': 'd15 id_location',
                                               'onFocus': 'WdatePicker({isShowClear:false,readOnly:true})',
            }
            ),
        }



