# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import os
from django.db.models.signals import post_save


def get_image_path(User, filename):
    return os.path.join('photos', str(User.id), filename)


GENDER_CHOICES = (
    (u'男', u'男'),
    (u'女', u'女'),
)


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, unique=True)
    avatar_big = models.ImageField(upload_to='avatar', verbose_name=u'大头像', blank=True, null=True,
                               default='avatar/default.png')
    avatar_middle = models.ImageField(upload_to='avatar', verbose_name=u'中头像', blank=True, null=True,
                               default='avatar/default.png')
    avatar_little = models.ImageField(upload_to='avatar', verbose_name=u'小头像', blank=True, null=True,
                               default='avatar/default.png')
    shorturl = models.CharField(max_length=20, verbose_name=u'域名', blank=True, null=True)
    nickname = models.CharField(max_length=20, verbose_name=u'昵称', blank=True, null=True)
    location = models.CharField(max_length=20, verbose_name=u'居住地', blank=True, null=True)
    birthday = models.DateField(verbose_name=u'生日', blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name=u'性别', blank=False, null=True,
                              default='')

    def user_post_save(sender, instance, created, **kwargs):
        """Create a user profile when a new user account is created"""
        if created == True:
            p = Profile()
            p.user = instance
            p.save()
            p.shorturl = p.user.id
            p.save()

    post_save.connect(user_post_save, sender=User)

