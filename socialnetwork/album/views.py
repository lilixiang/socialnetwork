# -*- coding: utf-8 -*-

# Create your views here.
from django.shortcuts import render_to_response
from socialnetwork.album.models import Album, Photo, PhotoComment
from socialnetwork.album.forms import AlbumForm, PhotoForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from socialnetwork.feed.views import navgation, paging
from socialnetwork.status.models import status
from socialnetwork.account.models import Profile, User
from socialnetwork.friend.models import Friends

import datetime, json


@login_required()
def album_create(request):
    content = {}
    profile = Profile.objects.get(user=request.user.id)

    nav = navgation(request)
    content['nav'] = nav

    follow = Friends.objects.filter(user=profile.user.id).order_by('created_time').reverse()
    follow_by = Friends.objects.filter(friend=profile.user.id).order_by('created_time').reverse()


    #渲染模板
    content['follow'] = follow
    content['follow_by'] = follow_by
    content['profile'] = profile

    if request.method == 'GET':
        form = AlbumForm()
        content['form'] = form
        return render_to_response('album_form.html', {'content': content}, context_instance=RequestContext(request))

    elif request.method == 'POST':
        form = AlbumForm(request.POST.copy())
        content['form'] = form
        if form.is_valid():
            if form.errors:


                return render_to_response('album_form.html', {'content': content},
                                          context_instance=RequestContext(request))
            else:
                now = datetime.datetime.now()
                album = form.save(commit=False)
                album.album_author = request.user
                album.album_date = now
                album.save()

                return HttpResponseRedirect('http://localhost/album/%s/' % (album.id))
        return render_to_response('album_form.html', {'content': content}, context_instance=RequestContext(request))


@login_required()
def album_edit(request, album_url):
    content = {}
    profile = Profile.objects.get(user=request.user.id)

    nav = navgation(request)
    content['nav'] = nav

    follow = Friends.objects.filter(user=profile.user.id).order_by('created_time').reverse()
    follow_by = Friends.objects.filter(friend=profile.user.id).order_by('created_time').reverse()


    #渲染模板
    content['follow'] = follow
    content['follow_by'] = follow_by
    content['profile'] = profile

    album = Album.objects.get(id=album_url)
    if album:
    # if int(album.album_author_id) == int(request.user.id):
        form = AlbumForm(instance=album)
        content['form'] = form

        nav = navgation(request)
        content['nav'] = nav

        if request.method == 'GET':
            return render_to_response('album_form.html', {'content': content},
                                      context_instance=RequestContext(request))


        elif request.method == 'POST':
            form = AlbumForm(data=request.POST or None, instance=album)
            content['form'] = form

            if form.is_valid():
                if form.errors:
                    return render_to_response('album_form.html', {'content': content},
                                              context_instance=RequestContext(request))
                else:
                    now = datetime.datetime.now()
                    album = form.save(commit=False)
                    album.album_author = request.user
                    album.album_date = now
                    album.save()

                    return HttpResponseRedirect('/album/%d/' % album.id)
            return render_to_response('album_form.html', {'content': content},
                                      context_instance=RequestContext(request))
            # else:#404!!!
            #     return render_to_response('404.html', context_instance=RequestContext(request))
    else:#404!!!
        return render_to_response('404.html', context_instance=RequestContext(request))


def album(request, album_url):
    album = Album.objects.get(id=album_url)
    people_url = album.album_author.get_profile().shorturl
    content = {}
    profile = Profile.objects.get(shorturl=people_url)
    photo = Photo.objects.filter(photo_album=album.id)

    nav = navgation(request)
    content['nav'] = nav

    follow = Friends.objects.filter(user=profile.user.id).order_by('created_time').reverse()
    follow_by = Friends.objects.filter(friend=profile.user.id).order_by('created_time').reverse()



    #分页使用
    n = 3
    photos, page_range = paging(request, photo, n)

    #渲染模板
    content['follow'] = follow
    content['follow_by'] = follow_by
    content['profile'] = profile
    content['photos'] = photos
    content['page_range'] = page_range

    follow_btn = {}
    content['profile'] = profile
    content['follow_btn'] = follow_btn
    if album:
        content['album'] = album

        try:
            user = request.user
        except Exception:
            user = User
        if user.is_authenticated():
            if user.id != profile.user_id:
                try:
                    friend = Friends.objects.get(user=user, friend=profile.shorturl)
                except Exception:
                    friend = None
                if not friend:
                    follow_btn['follow_url'] = 'http://localhost/people/%s/add' % people_url
                    follow_btn['type'] = u'关注'
                else:
                    follow_btn['follow_url'] = 'http://localhost/people/%s/del' % people_url
                    follow_btn['type'] = u'取消关注'
            else:
                follow_btn['type'] = None
                return render_to_response('album.html', {'content': content},
                                          context_instance=RequestContext(request))

        return render_to_response('album.html', {'content': content}, context_instance=RequestContext(request))
    else:#404!!!
        return render_to_response('404.html', context_instance=RequestContext(request))


def album_list(request, people_url):
    profile = Profile.objects.get(shorturl=people_url)

    album = Album.objects.filter(album_author=profile.user.id)

    if  profile:
    #if  note.note_authors.id == profile.user.id:
        if request.method == 'GET':
            content = {}

            follow = Friends.objects.filter(user=profile.user.id).order_by('created_time').reverse()
            follow_by = Friends.objects.filter(friend=profile.user.id).order_by('created_time').reverse()
            nav = navgation(request)
            content['nav'] = nav

            #分页使用
            n = 2
            albums, page_range = paging(request, album, n)


            #渲染模板
            content['albums'] = albums
            content['follow'] = follow
            content['follow_by'] = follow_by
            content['profile'] = profile
            content['page_range'] = page_range

            follow_btn = {'follow_url': 'http://localhost/people/%s/add' % people_url, 'type': u'关注', }
            content['profile'] = profile
            content['follow_btn'] = follow_btn

            try:
                user = request.user
            except Exception:
                user = User
            if user.is_authenticated():
                if user.id != profile.user_id:
                    try:
                        friend = Friends.objects.get(user=user, friend=profile.shorturl)
                    except Exception:
                        friend = None
                    if not friend:
                        follow_btn['follow_url'] = 'http://localhost/people/%s/add' % people_url
                        follow_btn['type'] = u'关注'
                    else:
                        follow_btn['follow_url'] = 'http://localhost/people/%s/del' % people_url
                        follow_btn['type'] = u'取消关注'
                else:
                    follow_btn['type'] = None
                    return render_to_response('album_list.html', {'content': content},
                                              context_instance=RequestContext(request))

            return render_to_response('album_list.html', {'content': content}, context_instance=RequestContext(request))
            #else:#404!!!
            #   return render_to_response('404.html',context_instance=RequestContext(request))
    else:#404!!!
        return render_to_response('404.html', context_instance=RequestContext(request))


def photo_upload(request, album_url):
    album = Album.objects.get(id=album_url)
    content = {}
    profile = Profile.objects.get(user=request.user.id)

    nav = navgation(request)
    content['nav'] = nav

    follow = Friends.objects.filter(user=profile.user.id).order_by('created_time').reverse()
    follow_by = Friends.objects.filter(friend=profile.user.id).order_by('created_time').reverse()


    #渲染模板
    content['follow'] = follow
    content['follow_by'] = follow_by
    content['profile'] = profile

    if album:
    #if int(album.album_author_id) == int(request.user.id):
        if request.method == 'GET':
            form = PhotoForm()
            content['form'] = form
            return render_to_response('photo_upload.html', {'content': content},
                                      context_instance=RequestContext(request))


        elif request.method == 'POST':
            form = PhotoForm(request.POST, request.FILES)
            photo = request.FILES['photo']

            content['form'] = form
            if form.is_valid():
                if form.errors:
                    return render_to_response('photo_upload.html', {'content': content},
                                              context_instance=RequestContext(request))
                else:

                    photo = form.save(commit=False)
                    now = datetime.datetime.now()
                    photo.photo_date = now
                    photo.photo_author = request.user
                    photo.photo_album = album
                    photo.save()

                    status(author=request.user,
                           content='<a href="http://localhost/album/%s/">%s</a>' % (album.id, album.album_title),
                           title=photo.photo.url,
                           date=now,
                           type=u'Photo',
                           url=u'photo/%d/' % photo.id)

                    return HttpResponseRedirect('http://localhost/album/%d/' % album.id)
            return render_to_response('photo_upload.html', {'content': content},
                                      context_instance=RequestContext(request))

            #else:#404!!!
            #    return render_to_response('404.html', context_instance=RequestContext(request))
    else:#404!!!
        return render_to_response('404.html', context_instance=RequestContext(request))


def photo(request, photo_url):
    photo = Photo.objects.get(id=photo_url)
    content = {}
    profile = Profile.objects.get(user=photo.photo_author.id)
    album = Album.objects.get(id=photo.photo_album.id)

    nav = navgation(request)
    content['nav'] = nav

    follow = Friends.objects.filter(user=profile.user.id).order_by('created_time').reverse()
    follow_by = Friends.objects.filter(friend=profile.user.id).order_by('created_time').reverse()


    #渲染模板
    content['follow'] = follow
    content['follow_by'] = follow_by
    content['profile'] = profile
    content['album'] = album


    follow_btn = {}
    content['profile'] = profile
    content['follow_btn'] = follow_btn
    if photo:
        content['photo'] = photo

        try:
            user = request.user
        except Exception:
            user = User
        if user.is_authenticated():
            if user.id != profile.user_id:
                try:
                    friend = Friends.objects.get(user=user, friend=profile.shorturl)
                except Exception:
                    friend = None
                if not friend:
                    follow_btn['follow_url'] = 'http://localhost/people/%s/add' % profile.shorturl
                    follow_btn['type'] = u'关注'
                else:
                    follow_btn['follow_url'] = 'http://localhost/people/%s/del' % profile.shorturl
                    follow_btn['type'] = u'取消关注'
            else:
                follow_btn['type'] = None

    if photo:
    #if int(album.album_author_id) == int(request.user.id):
        if request.method == 'GET':
            content['photo'] = photo

            return render_to_response('photo.html', {'content': content}, context_instance=RequestContext(request))
            # else:#404!!!
            #     return render_to_response('404.html', context_instance=RequestContext(request))
    else:#404!!!
        return render_to_response('404.html', context_instance=RequestContext(request))


@login_required()
def photo_comment(request, photo_url):
    photo = Photo.objects.get(pk=photo_url)
    user = request.user

    if request.method == 'GET':
        comment = PhotoComment.objects.filter(comment_photo=photo_url)
        content = {}

        content['comments'] = comment
        return render_to_response('photo_comment_form.html', {'content': content},
                                  context_instance=RequestContext(request))


    elif request.method == 'POST':

        txt = request.POST.get("comment", '')
        comment = PhotoComment()
        comment.comment_author = user
        comment.comment_photo = photo
        comment.comment_content = txt
        comment.comment_date = datetime.datetime.now()
        comment.save()

        response_data = {}
        response_data['comment'] = comment.comment_content
        response_data['comment_author_url'] = comment.comment_author.get_profile().shorturl
        response_data['comment_author_nickname'] = comment.comment_author.get_profile().nickname

        return HttpResponse(json.dumps(response_data), mimetype="application/json")

