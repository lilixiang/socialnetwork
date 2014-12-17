# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


TYPE_CHOICES = (
                (u'Note', u'日记'),
                (u'Status', u'状态'),
                (u'Photo', u'照片'),
                (u'ReT', u'转发'),
    )
class Status(models.Model):
    status_content = models.TextField(verbose_name=u'正文',blank=True,null=True)
    status_author = models.ForeignKey(User,verbose_name=u'作者',related_name="status_author_set")
    status_type = models.CharField(max_length=10,choices = TYPE_CHOICES,verbose_name=u'类型', blank=False, default='')
    status_title = models.CharField(verbose_name=u'推送标题',max_length=200, blank=True,null=True)
    status_url = models.CharField(verbose_name=u'推送链接',max_length=200,blank=True,null=True)
    status_date = models.DateTimeField(verbose_name=u'日期')

class Comment(models.Model):
    comment_status = models.ForeignKey(Status,verbose_name=u'评论状态')
    comment_content = models.CharField(verbose_name=u'正文',max_length=140)
    comment_author = models.ForeignKey(User,verbose_name=u'作者')
    comment_date = models.DateTimeField(verbose_name=u'日期')



def status(author,content,title,date,type,url):
    f = Status()
    f.status_author = author
    f.status_content = content
    f.status_title = title
    f.status_date = date
    f.status_type = type
    f.status_url = url
    f.save()