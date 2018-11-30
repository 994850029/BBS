from django.db import models

from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserInfo(AbstractUser):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=16)
    avatar = models.FileField(upload_to='avatar/', default='avatar/default.png')
    create_date = models.DateTimeField(auto_now_add=True)
    blog = models.OneToOneField(to='Blog', to_field='id',null=True,blank=True)
    class Meta:
        # admin中显示表名
        verbose_name='用户表'
        # admin中表名s去掉
        verbose_name_plural=verbose_name


class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, null=True,blank=True)
    site_name = models.CharField(max_length=64)
    theme = models.CharField(max_length=64)
    class Meta:
        verbose_name = '博客'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.site_name


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    blog = models.ForeignKey(to='Blog', to_field='id', null=True,blank=True)


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    blog = models.ForeignKey(to='Blog', to_field='id', null=True,blank=True)


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    desc = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    commit_num = models.IntegerField(default=0)
    up_num = models.IntegerField(default=0)
    down_num = models.IntegerField(default=0)
    content = models.TextField()
    category = models.ForeignKey(to='Category', to_field='id', null=True,blank=True)
    blog = models.ForeignKey(to='Blog', to_field='id', null=True,blank=True)
    tag = models.ManyToManyField(to='Tag', through='ArticleToTag', through_fields=('article', 'tag'))
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.title

class ArticleToTag(models.Model):
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(to='Article', to_field='id')
    tag = models.ForeignKey(to='Tag', to_field='id')


class Commit(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='UserInfo', to_field='id')
    article = models.ForeignKey(to='Article', to_field='id')
    content = models.TextField()
    commit_time = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(to='self', to_field='id', null=True)
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
class UpAndDown(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='UserInfo', to_field='id')
    article = models.ForeignKey(to='Article', to_field='id')
    is_up = models.BooleanField()

    class Meta:
        unique_together = (('user', 'article'),)
