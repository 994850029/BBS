from django.db import models

from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserInfo(AbstractUser):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=16)
    avatar = models.FileField(upload_to='static/avatar/', default='/static/img/default.png')
    create_date = models.DateTimeField(auto_now_add=True)
    blog = models.OneToOneField(to='Blog', to_field='id',null=True)


class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, null=True)
    site_name = models.CharField(max_length=64)
    theme = models.CharField(max_length=64)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    blog = models.ForeignKey(to='Blog', to_field='id', null=True)


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    blog = models.ForeignKey(to='Blog', to_field='id', null=True)


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    desc = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    category = models.ForeignKey(to='Category', to_field='id', null=True)
    blog = models.ForeignKey(to='Blog', to_field='id', null=True)

    tag = models.ManyToManyField(to='Tag', through='ArticleToTag', through_fields=('article', 'tag'))


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


class UpAndDown(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='UserInfo', to_field='id')
    article = models.ForeignKey(to='Article', to_field='id')
    is_up = models.BooleanField()

    class Meta:
        unique_together = (('user', 'article'),)
