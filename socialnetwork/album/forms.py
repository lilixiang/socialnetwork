# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import auth
from  socialnetwork.album.models import Album, Photo


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = ('album_author', 'album_date','album_privacy','album_comment')
        widgets = {
            'album_privacy': forms.RadioSelect(attrs={'class': 'radio inline'}),
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ('photo_author', 'photo_date', 'photo_album')
        widgets = {
            'photo': forms.FileInput(),
        }