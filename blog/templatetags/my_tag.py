from django.template import Library
from blog import models
from django.db.models import Count
from django.db.models.functions import TruncMonth

register = Library()


@register.inclusion_tag('left_fold.html')
def left_fold(username):
    user = models.UserInfo.objects.filter(username=username).first()
    blog = user.blog
    category_num = models.Category.objects.filter(blog=blog).all().annotate(coun=Count('article__title')).values_list(
        'title', 'coun', 'id')
    tag_num = models.Tag.objects.filter(blog=blog).all().annotate(coun=Count('article__title')).values_list('title',
                                                                                                            'coun',
                                                                                                            'id')
    y_m_num = models.Article.objects.all().filter(blog=blog).annotate(y_m=TruncMonth('create_time')).values(
        'y_m').annotate(
        coun=Count('y_m')).values_list('y_m', 'coun')

    return {'category_num': category_num, 'tag_num': tag_num, 'y_m_num': y_m_num, 'username': username,'blog':blog}
