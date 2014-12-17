# -*- coding: utf-8 -*-
from django import forms
from  socialnetwork.status.models import Status,Comment

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        exclude = ('status_author','status_date','status_type','status_title','status_url')
        widgets = {
            'status_content': forms.Textarea(attrs={'class':'span6'}),

            }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('comment_status','comment_author','comment_date',)
        widgets = {
            }