# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

PRIVACY_CHOICES= (
        (u'P', u'对所有人公开'),
        (u'F', u'对好友公开'),
        (u'M', u'仅自己可见'),
        )
class Note(models.Model):
    note_title = models.CharField(max_length=20,verbose_name=u'标题')
    note_authors = models.ForeignKey(User,verbose_name=u'作者')
    note_date = models.DateTimeField(verbose_name=u'日期')
    note_privacy = models.CharField(max_length=1,choices = PRIVACY_CHOICES,verbose_name=u'可见性', blank=False, null=True,default='P')
    note_comment = models.BooleanField(verbose_name=u'权限')
    note_content = models.TextField(verbose_name=u'正文')




class NoteComment(models.Model):
    comment_note = models.ForeignKey(Note,verbose_name=u'评论日记')
    comment_content = models.CharField(verbose_name=u'正文',max_length=140)
    comment_author = models.ForeignKey(User,verbose_name=u'作者')
    comment_date = models.DateTimeField(verbose_name=u'日期')