from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from blog import common
from django.contrib import auth
from blog import models
import datetime
import hashlib
from django.contrib.auth.decorators import login_required


# Create your views here.
def login(request):
    if request.method == 'GET':
        print(request.session.get('yzm'))
        return render(request, 'login.html')
    if request.method == 'POST':
        # blog = models.Blog.objects.create(site_name='test',theme='test')
        # models.UserInfo.objects.create_user(username='zjh',password='123',phone='12345',blog=blog)
        # msg = json.loads(request.body.decode('utf-8'))
        response = {'status': 100, 'msg': None}
        msg = request.POST
        name = msg.get('name')
        pwd = msg.get('pwd')
        yzm_session = request.session.get('yzm')
        yzm = msg.get('yzm')

        user = auth.authenticate(username=name, password=pwd)
        if user and yzm.upper() == yzm_session.upper():
            # return HttpResponse(json.dumps('登录成功!'))
            auth.login(request, user)
            return JsonResponse(response)
        else:
            # return HttpResponse(json.dumps('用户名或者密码错误!'))
            response['status'] = 101
            response['msg'] = '用户名或者密码错误!'
            return JsonResponse(response)


def get_img(request):
    if not request.META.get('QUERY_STRING'):
        request.session['count'] = 1
    else:
        request.session['count'] += 1
    img = Image.new('RGB', (300, 30), color=common.get_random_color())
    font = ImageFont.truetype(font='static/font/txt.TTF', size=24)
    img_draw = ImageDraw.Draw(img)
    font_content = common.get_random_yzm(5)
    request.session['yzm'] = font_content
    img_draw.text((100, 0), font_content, common.get_random_color(), font=font)
    common.add_dianxiang(300, 30, img_draw, int(5 / request.session['count']), int(60 / (request.session['count'] + 2)))
    f = BytesIO()
    img.save(f, 'png')
    data = f.getvalue()

    return HttpResponse(data)


def register(request):
    if request.method == 'GET':
        forms = common.RegisterForm()
        return render(request, 'register.html', locals())
    elif request.is_ajax():
        response = {'status': 100, 'msg': None}
        user = common.RegisterForm(request.POST)
        files = request.FILES.get('img')

        if user.is_valid():
            dic = user.cleaned_data
            dic.pop('re_password')
            files = request.FILES.get('img')
            if files:
                hs = hashlib.md5()
                time = datetime.datetime.now()
                hs.update(str(time).encode('utf-8'))
                files.name = hs.hexdigest() + '.png'
                dic['avatar'] = files
            models.UserInfo.objects.create_user(**dic)
        else:
            response['status'] = 101
            response['msg'] = user.errors
            # print(user.errors)
        return JsonResponse(response)


def user_blur(request):
    response = {'status': 100, 'msg': None}
    username = request.POST.get('username')
    user = models.UserInfo.objects.filter(username=username).first()
    if user:
        response['status'] = 101
        response['msg'] = '用户名已存在!'
    return JsonResponse(response)


def index(request):
    if request.method == 'GET':
        articles = models.Article.objects.all().order_by('-create_time')
        return render(request, 'index.html', locals())


def user_logout(request):
    auth.logout(request)
    return redirect('/index/')


# def header_img(request,id):
#     img_path = models.UserInfo.objects.filter(blog__article__id=id).first().avatar
#
#     if str(img_path).startswith('avatar'):
#         img = Image.new('RGB', (300, 30), color=common.get_random_color())
#         return HttpResponse(img)
#     else:
#         return HttpResponse(str(img_path))

@login_required
def set_pwd(request):
    if request.method == 'GET':
        forms = common.SetPwdForm()
        return render(request, 'setpwd.html', locals())
    if request.is_ajax():
        response = {'status': 100, 'msg': None}
        name = request.user.username
        pwd_dic = request.POST
        old_pwd = pwd_dic.get('old_password')
        user = auth.authenticate(username=name, password=old_pwd)
        pwd = common.SetPwdForm(pwd_dic)
        if user and pwd.is_valid():
            user.set_password(pwd.cleaned_data.get('new_password'))
            user.save()
            auth.logout(request)
        if not user:
            response['status2'] = 102
            response['msg2'] = '旧密码错误!'

        if not pwd.is_valid():
            response['status'] = 101
            response['msg'] = pwd.errors

        return JsonResponse(response)
