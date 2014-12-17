# -*- coding: utf-8 -*-
from django import forms

from  socialnetwork.board.models import Board



class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        exclude  = ('message_author','message_date')
        widgets = {
            'message_content': forms.Textarea(attrs={'class':'span6'}),
            'board_belong': forms.HiddenInput(),
            }
