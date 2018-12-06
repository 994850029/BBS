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
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.db.models import F
from django.db import transaction
import json
from django.core.paginator import Paginator
from bs4 import BeautifulSoup
import os
from BBS01 import settings
from threading import Thread
from django.core.mail import send_mail


# Create your views here.
def login(request):
    if request.method == 'GET':
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
    img = Image.new('RGB', (300, 30), (255, 255, 255))
    font = ImageFont.truetype(font='static/font/txt.TTF', size=24)
    img_draw = ImageDraw.Draw(img)
    font_content = common.get_random_yzm(5)
    request.session['yzm'] = font_content
    img_draw.text((100, 0), font_content, common.get_random_color(), font=font)
    common.add_dianxiang(300, 30, img_draw, int(5 / request.session['count']), int(60 / (request.session['count'])))
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
            with transaction.atomic():
                blog = models.Blog.objects.create(title=dic.get('username') + '的博客', site_name=dic.get('username'),
                                                  theme='3.css')
                dic['blog'] = blog
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
        paginator = Paginator(articles, 5)
        try:
            if int(request.GET.get('page')) not in range(1, paginator.num_pages + 1):
                page_num = 1
            else:
                page_num = int(request.GET.get('page'))
        except Exception as e:
            page_num = 1
        page_content = paginator.page(page_num)
        if paginator.num_pages < 6:
            page_count = paginator.page_range
        else:
            if page_num - 3 < 1:
                page_count = range(1, 6)
            elif page_num + 3 > paginator.num_pages:
                page_count = range(paginator.num_pages - 4, paginator.num_pages + 1)
            else:
                page_count = range(page_num - 2, page_num + 3)

        return render(request, 'index.html', locals())


def user_logout(request):
    auth.logout(request)
    return redirect('/index/')


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
        user = request.user
        userpwd = user.check_password(old_pwd)
        pwd = common.SetPwdForm(pwd_dic)
        if userpwd and pwd.is_valid():
            user.set_password(pwd.cleaned_data.get('new_password'))
            user.save()
            auth.logout(request)
        if not userpwd:
            response['status2'] = 102
            response['msg2'] = '旧密码错误!'

        if not pwd.is_valid():
            response['status'] = 101
            response['msg'] = pwd.errors
        return JsonResponse(response)


@login_required
def set_re_password(request):
    response = {'status': 100, 'msg': None}
    old_password = request.POST.get('old_password')
    user = request.user
    user_pwd = user.check_password(old_password)
    if not user_pwd:
        response['status'] = 101
        response['msg'] = '旧密码错误!'
    return JsonResponse(response)


def img_update(request):
    if request.user.is_authenticated():
        file = request.FILES.get('img')
        if file:
            hs = hashlib.md5()
            time = datetime.datetime.now()
            hs.update(str(time).encode('utf-8'))
            file.name = hs.hexdigest() + '.png'
        user = models.UserInfo.objects.filter(id=request.user.id).first()
        # 删除原来的头像
        path = os.path.join(settings.MEDIA_ROOT, 'avatar', str(user.avatar).split('/')[1])
        os.remove(path)
        user.avatar = file
        user.save()
        return JsonResponse({'status': 100})
    else:
        return JsonResponse({'status': 101})


def error(request):
    return render(request, 'error.html')


def user_blog(request, username, *args, **kwargs):
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return render(request, 'error.html')
    blog = user.blog
    article_list = blog.article_set.all()
    if kwargs.get('condition') == 'category':
        article_list = article_list.filter(category__id=kwargs.get('id'))
    elif kwargs.get('condition') == 'tag':
        article_list = article_list.filter(tag__id=kwargs.get('id'))
    elif kwargs.get('condition') == 'archive':
        time_list = kwargs.get('id').split('-')
        article_list = article_list.filter(create_time__year=time_list[0], create_time__month=time_list[1])
    category_num = models.Category.objects.filter(blog=blog).all().annotate(coun=Count('article__title')).values_list(
        'title', 'coun', 'id')
    tag_num = models.Tag.objects.filter(blog=blog).all().annotate(coun=Count('article__title')).values_list('title',
                                                                                                            'coun',
                                                                                                            'id')
    y_m_num = models.Article.objects.all().filter(blog=blog).annotate(y_m=TruncMonth('create_time')).values(
        'y_m').annotate(
        coun=Count('y_m')).values_list('y_m', 'coun')
    return render(request, 'user_blog.html', locals())


def article_content(request, username, id):
    username = username
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return render(request, 'error.html')
    blog = user.blog
    article = models.Article.objects.filter(id=id).first()
    if not article:
        return render(request, 'error.html')
    content_list = models.Commit.objects.filter(article=article).all()
    return render(request, 'article_content.html', locals())


@login_required
def up_and_down(request):
    dic = request.POST
    response = {'status': 100, 'msg': None}
    article_id = dic.get('article_id')
    is_up = dic.get('is_up')
    is_up = json.loads(is_up)
    if request.user.is_authenticated():
        user_cf = models.UpAndDown.objects.filter(user=request.user, article_id=article_id).first()
        if user_cf:
            response['msg'] = '无法多次点赞或者点踩哦!'
            response['status'] = 101
            return JsonResponse(response)
        else:
            with transaction.atomic():
                models.UpAndDown.objects.create(user=request.user, article_id=article_id, is_up=is_up)
                article = models.Article.objects.filter(id=article_id)
            if is_up:
                article.update(up_num=F('up_num') + 1)
                response['status'] = 100
                response['msg'] = '您已成功点赞!'
            else:
                article.update(down_num=F('down_num') + 1)
                response['status'] = 100
                response['msg'] = '您已成功反对!'
    else:
        response['status'] = 101
        response['msg'] = '请先登录!'
    return JsonResponse(response)


def commit(request):
    if request.is_ajax():
        response = {'status': 100, 'msg': None}
        if request.user.is_authenticated():
            dic = request.POST
            user = request.user
            parent_id = dic.get('parent_id')
            article_id = dic.get('article_id')
            content = dic.get('content')
            with transaction.atomic():
                commit_obj = models.Commit.objects.create(content=content, article_id=article_id, parent_id=parent_id,
                                                          user=user)
                models.Article.objects.filter(id=article_id).update(commit_num=F('commit_num') + 1)
            response['time'] = commit_obj.commit_time.strftime('%Y-%m-%d %X')
            response['content'] = commit_obj.content
            response['username'] = commit_obj.user.username
            # mail = Thread(target=send_mail,args=('您的文章被评论了','评论的内容测试',settings.EMAIL_HOST_USER,['zhoujianhao1996@foxmail.com']))
            # mail.start()

            response['msg'] = '评论成功!'
            if parent_id:
                # 如果是字评论,返回父评论的名字
                response['parent_name'] = commit_obj.parent.user.username

        else:
            response['status'] = 101
            response['msg'] = '您的请求非法'
        return JsonResponse(response)


@login_required
def article_manage(request):
    if request.method == 'GET':
        user = request.user
        articles = models.Article.objects.filter(blog=user.blog).all()
        return render(request, 'article_manage.html', locals())


def article_del(request):
    if request.user.is_authenticated():
        article_id = request.GET.get('article_id')
        models.Article.objects.filter(id=article_id).delete()
        return redirect('/article_manage/')
    else:
        return redirect('/error/')


@login_required
def add_article(request):
    if request.user.is_authenticated():
        if request.method == 'GET':
            return render(request, 'add_article.html')
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            content_bs = BeautifulSoup(content, 'html.parser')
            tags = content_bs.find_all()
            for tag in tags:
                if tag.name == 'script':
                    tag.decompose()
            desc = content_bs.text[:100] + '...'
            models.Article.objects.create(title=title, desc=desc, content=str(content_bs), blog=request.user.blog)
            return redirect('/article_manage/')
    else:
        return redirect('/error/')


def article_img(request):
    if request.user.is_authenticated():
        img = request.FILES.get('myfile')
        path = os.path.join(settings.BASE_DIR, 'media', 'img')
        if not os.path.isdir(path):
            os.mkdir(path)
        hs = hashlib.md5()
        time = datetime.datetime.now()
        msg = str(time) + img.name
        hs.update(msg.encode('utf-8'))
        img_name = hs.hexdigest() + '.png'
        img_path = os.path.join(path, img_name)
        with open(img_path, 'wb') as f:
            for file in img:
                f.write(file)
        dic = {'error': 0, 'url': '/media/img/%s' % img_name}
        return JsonResponse(dic)
    else:
        return redirect('/error/')


@login_required
def article_update(request, article_id):
    if request.user.is_authenticated():
        if request.method == 'GET':
            article = models.Article.objects.filter(id=article_id).first()
            return render(request, 'article_update.html', locals())
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            content_bs = BeautifulSoup(content, 'html.parser')
            tags = content_bs.find_all()
            for tag in tags:
                if tag.name == 'script':
                    tag.decompose()
            desc = content_bs.text[:100] + '...'
            models.Article.objects.filter(id=article_id).update(title=title, desc=desc, content=str(content_bs))
            return redirect('/article_manage/')
    else:
        return redirect('/error/')
