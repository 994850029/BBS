from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from blog import common
from django.contrib import auth
from blog import models
import datetime
import hashlib


# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        # blog = models.Blog.objects.create(site_name='test',theme='test')
        # models.UserInfo.objects.create_user(username='zjh',password='123',phone='12345',blog=blog)
        # msg = json.loads(request.body.decode('utf-8'))
        msg = request.POST
        name = msg.get('name')
        pwd = msg.get('pwd')
        yzm_session = request.session.get('yzm')
        yzm = msg.get('yzm')
        print(yzm_session)
        user = auth.authenticate(username=name, password=pwd)
        if user and yzm.upper() == yzm_session.upper():
            # return HttpResponse(json.dumps('登录成功!'))
            auth.login(request, user)
            return HttpResponse('登录成功!')
        else:
            # return HttpResponse(json.dumps('用户名或者密码错误!'))
            return HttpResponse('用户名或者密码错误!')

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
    common.add_dianxiang(300, 30, img_draw,int(5/request.session['count']),int(60/(request.session['count']+2)))
    f = BytesIO()
    img.save(f, 'png')
    data = f.getvalue()

    return HttpResponse(data)


def register(request):
    if request.method == 'GET':
        forms = common.RegisterForm()
        return render(request, 'register.html', locals())
    elif request.is_ajax():
        response = {'status':100,'msg':None}
        user = common.RegisterForm(request.POST)
        files = request.FILES.get('img')

        if user.is_valid():
            dic=user.cleaned_data
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
    response = {'status':100,'msg':None}
    username = request.POST.get('username')
    user = models.UserInfo.objects.filter(username=username).first()
    if user:
        response['status'] = 101
        response['msg'] = '用户名已存在!'
    return JsonResponse(response)