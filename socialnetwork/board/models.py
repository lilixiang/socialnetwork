# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User



class Board(models.Model):
    board_belong = models.ForeignKey(User, verbose_name=u'留言板归属',related_name="board_belong_set")
    message_author = models.ForeignKey(User, verbose_name=u'留言人',related_name="message_author_set")
    message_date = models.DateTimeField(verbose_name=u'留言日期')
    message_content = models.TextField(verbose_name=u'留言内容', max_length=200)


