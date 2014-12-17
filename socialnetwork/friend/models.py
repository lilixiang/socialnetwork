from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Group(models.Model):
    user = models.ForeignKey(User)
    group_id = models.SmallIntegerField()
    group_name = models.CharField(max_length=100)


class Friends(models.Model):
    user = models.ForeignKey(User, related_name="friendship_creator_set")
    friend = models.ForeignKey(User, related_name="friend_set")
    block = models.CharField(max_length=100,blank=None,null=None)
    group = models.ManyToManyField(Group,blank=None,null=None)
    visibility = models.CharField(max_length=100,blank=None,null=None)
    created_time = models.DateTimeField()

    class Meta:
        db_table = 'friend_relation'

    def __str__(self):
       return self.friend.get_profile().nickname