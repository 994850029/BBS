from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO
from static.common import common
from django.contrib import auth
from blog import models
import json


# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    if request.method == 'POST':
        # blog = models.Blog.objects.create(site_name='test',theme='test')
        # models.UserInfo.objects.create_user(username='zjh',password='123',phone='12345',blog=blog)
        msg = json.loads(request.body.decode('utf-8'))
        user = msg.get('name')
        pwd = msg.get('pwd')
        yzm_session = request.session.get('yzm')
        yzm = msg.get('yzm')
        pd = auth.authenticate(username=user,password=pwd)
        if pd and yzm == yzm_session:
            return HttpResponse(json.dumps('登录成功!'))
        else:
            return HttpResponse(json.dumps('用户名或者密码错误!'))


def get_img(request):
    img = Image.new('RGB',(300,30),color=common.get_random_color())
    font = ImageFont.truetype(font='static/font/txt.TTF',size=18)
    img_draw = ImageDraw.Draw(img)
    font_content = common.get_random_yzm(5)

    request.session['yzm'] = font_content
    img_draw.text((100,0),font_content,common.get_random_color(),font=font)
    f= BytesIO()
    img.save(f,'png')
    data = f.getvalue()

    return HttpResponse(data)
