# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import datetime, random, time
import os
# Create your models here.
PRIVACY_CHOICES = (
    (u'P', u'对所有人公开'),
    (u'F', u'对好友公开'),
    (u'M', u'仅自己可见'),
)


class Album(models.Model):
    album_title = models.CharField(max_length=20, verbose_name=u'标题')
    album_author = models.ForeignKey(User, verbose_name=u'作者')
    album_date = models.DateTimeField(verbose_name=u'日期')
    album_privacy = models.CharField(max_length=1, choices=PRIVACY_CHOICES, verbose_name=u'可见性', blank=False, null=True,
                                     default='P')
    album_comment = models.BooleanField(verbose_name=u'权限')


def content_file_name(instance, filename):
    t = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    f, ext = os.path.splitext(filename)
    return 'photo/%s%s%s' % (t, random.randint(1, 1000), ext)


class Photo(models.Model):
    photo_author = models.ForeignKey(User, verbose_name=u'作者', related_name="photo_author_set")
    photo_date = models.DateTimeField(verbose_name=u'日期')
    photo = models.ImageField(upload_to=content_file_name, verbose_name=u'照片', blank=True, null=True)
    photo_album = models.ForeignKey(Album, verbose_name=u'相册', related_name="photo_album_set")


class PhotoComment(models.Model):
    comment_photo = models.ForeignKey(Photo,verbose_name=u'评论照片')
    comment_content = models.CharField(verbose_name=u'正文',max_length=140)
    comment_author = models.ForeignKey(User,verbose_name=u'作者')
    comment_date = models.DateTimeField(verbose_name=u'日期')