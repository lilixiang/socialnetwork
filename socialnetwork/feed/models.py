# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import datetime


TYPE_CHOICES = (
                (u'Note', u'日记'),
                (u'Status', u'状态'),
                (u'Photo', u'照片'),
    )

# Create your models here.
class Feed(models.Model):
    feed_type = models.CharField(max_length=10,choices = TYPE_CHOICES,verbose_name=u'类型', blank=False, default='')
    feed_title = models.CharField(verbose_name=u'推送标题',max_length=200, blank=True,null=True)
    feed_url = models.CharField(verbose_name=u'推送链接',max_length=200,blank=True,null=True)
    feed_content = models.TextField(verbose_name=u'推送内容',blank=True,null=True)
    feed_author = models.ForeignKey(User,verbose_name=u'作者')
    feed_date = models.DateTimeField(verbose_name=u'日期')

class Update(models.Model):
    update_user = models.ForeignKey(User,verbose_name=u'更新用户')
    update_date = models.DateTimeField(verbose_name=u'日期')

    def user_post_save(sender, instance, created, **kwargs):
        """Create a user profile when a new user account is created"""
        if created == True:
            u = Update()
            u.update_user = instance
            u.update_date = datetime.datetime.now()
            u.save()
    post_save.connect(user_post_save, sender=User)


