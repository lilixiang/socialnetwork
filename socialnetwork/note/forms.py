# -*- coding: utf-8 -*-
from django import forms
from  socialnetwork.note.models import Note,NoteComment

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude = ('note_authors','note_date','note_privacy', 'note_authors','note_comment')
        widgets = {
            'note_title': forms.TextInput(attrs={'class':'span4'}),
            'note_content': forms.Textarea(attrs={'class':'span4'}),
            }

class NoteCommentForm(forms.ModelForm):
    class Meta:
        model = NoteComment
        exclude = ('comment_note','comment_author','comment_date',)
        widgets = {
            'comment_content': forms.Textarea(attrs={'class':'span6'}),

            }