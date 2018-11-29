import random
from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from blog import models


def get_random_color():
    return (
        random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    )


def get_random_yzm(i):
    res = ''
    for j in range(i):
        num = str(random.randint(0, 9))
        S = chr(random.randint(65, 90))
        s = chr(random.randint(97, 122))
        c = random.choice([num, S, s])
        res += c

    return res


def add_dianxiang(width, height, img_draw, xian_count, dian_count):
    for i in range(xian_count):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        # 在图片上画线
        img_draw.line((x1, y1, x2, y2), fill=get_random_color())

    for i in range(dian_count):
        # 画点
        img_draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        # 画弧形
        img_draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=3, required=True,
                               label='用户名',
                               widget=widgets.TextInput(attrs={'class': 'form-control'}),
                               error_messages={'max_length': '最大长度是20', 'min_length': '最短长度是3', 'required': '不能为空'})
    password = forms.CharField(max_length=20, min_length=3, required=True,
                               label='密码',
                               widget=widgets.PasswordInput(attrs={'class': 'form-control'}),
                               error_messages={'max_length': '最大长度是20', 'min_length': '最短长度是3', 'required': '不能为空'})
    re_password = forms.CharField(max_length=20, min_length=3, required=True,
                                  label='确认密码',
                                  widget=widgets.PasswordInput(attrs={'class': 'form-control'}),
                                  error_messages={'max_length': '最大长度是20', 'min_length': '最短长度是3', 'required': '不能为空'})
    phone = forms.CharField(max_length=11, min_length=4, label='电话', required=True,
                            widget=widgets.TextInput(attrs={'class': 'form-control'}),
                            error_messages={'max_length': '最大长度是11', 'min_length': '最短长度是4', 'required': '不能为空'})

    def clean_username(self):
        user = self.cleaned_data.get('username')
        pd = models.UserInfo.objects.filter(username=user).first()
        if pd:
            raise ValidationError('用户已存在!')
        else:
            return user

    def clean(self):
        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_password')
        if pwd == re_pwd:
            return self.cleaned_data
        else:
            raise ValidationError('两次密码不一致!')


class SetPwdForm(forms.Form):
    new_password = forms.CharField(max_length=20, min_length=3, required=True,
                                   label='输入新密码:',
                                   widget=widgets.PasswordInput(attrs={'class': 'form-control'}),
                                   error_messages={'max_length': '最大长度是20', 'min_length': '最短长度是3', 'required': '不能为空'})

    re_new_password = forms.CharField(max_length=20, min_length=3, required=True,
                                      label='确认新密码:',
                                      widget=widgets.PasswordInput(attrs={'class': 'form-control'}),
                                      error_messages={'max_length': '最大长度是20', 'min_length': '最短长度是3',
                                                      'required': '不能为空'})

    def clean(self):
        pwd = self.cleaned_data.get('new_password')
        re_pwd = self.cleaned_data.get('re_new_password')
        if pwd == re_pwd:
            return self.cleaned_data
        else:
            raise ValidationError('两次密码不一致!')
