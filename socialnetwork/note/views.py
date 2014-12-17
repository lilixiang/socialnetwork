# -*- coding: utf-8 -*-


# Create your views here.
from django.shortcuts import render_to_response
from socialnetwork.note.models import Note, NoteComment
from socialnetwork.note.forms import NoteCommentForm
from socialnetwork.account.models import Profile, User
from socialnetwork.friend.models import Friends

from socialnetwork.note.forms import NoteForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from socialnetwork.feed.views import navgation, paging
from socialnetwork.status.models import status,Status

import datetime, json


@login_required()
def note_create(request, people_url):
    profile = Profile.objects.get(shorturl=people_url)

    content = {}

    nav = navgation(request)
    content['nav'] = nav

    follow = Friends.objects.filter(user=profile.user.id).order_by('created_time').reverse()
    follow_by = Friends.objects.filter(friend=profile.user.id).order_by('created_time').reverse()


    #渲染模板
    content['notes'] = notes
    content['follow'] = follow
    content['follow_by'] = follow_by
    content['profile'] = profile

    if request.method == 'GET':
        form = NoteForm()
        content['form'] = form
        return render_to_response('note_form.html', {'content': content}, context_instance=RequestContext(request))

    elif request.method == 'POST':
        form = NoteForm(request.POST.copy())
        content['form'] = form
        if form.is_valid():
            if form.errors:
                return render_to_response('note_form.html', {'content': content},
                                          context_instance=RequestContext(request))
            else:
                now = datetime.datetime.now()
                note = form.save(commit=False)
                note.note_authors = request.user
                note.note_date = now
                note.save()
                status(author=request.user,
                       content=form.cleaned_data.get('note_content'),
                       title=form.cleaned_data.get('note_title'),
                       date=now,
                       type=u'Note',
                       url='note/%s/' % (note.id))

                return HttpResponseRedirect('http://localhost/people/%s/note/%s/' % (people_url,note.id))
        return render_to_response('note_form.html', {'content': content}, context_instance=RequestContext(request))


@login_required()
def note_edit(request,people_url, note_url):
    profile = Profile.objects.get(shorturl=people_url)
    note = Note.objects.get(id=note_url)

    content = {}

    nav = navgation(request)
    content['nav'] = nav

    follow = Friends.objects.filter(user=profile.user.id).order_by('created_time').reverse()
    follow_by = Friends.objects.filter(friend=profile.user.id).order_by('created_time').reverse()

    #渲染模板
    content['notes'] = notes
    content['follow'] = follow
    content['follow_by'] = follow_by



    follow_btn = {}
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


    if note and profile:
    #if note.note_authors.id == profile.user.id:
        form = NoteForm(instance=note)
        content['form'] = form

        if request.method == 'GET':
            return render_to_response('note_form.html', {'content': content},
                                      context_instance=RequestContext(request))
        elif request.method == 'POST':
            form = NoteForm(data=request.POST or None, instance=note)
            content['form'] = form
            if form.is_valid():
                if form.errors:
                    return render_to_response('note_form.html', {'content': content},
                                              context_instance=RequestContext(request))
                else:
                    now = datetime.datetime.now()
                    note = form.save(commit=False)
                    note.note_date = now
                    note.save()
                    return HttpResponseRedirect('http://localhost/people/%s/note/%s/' % (profile.shorturl, note.id))
            return render_to_response('note_form.html', {'content': content},
                                      context_instance=RequestContext(request))
            # else:#404!!!
            #     return render_to_response('404.html', context_instance=RequestContext(request))
    else:#404!!!
        return render_to_response('404.html', context_instance=RequestContext(request))



def note(request, people_url, note_url):
    profile = Profile.objects.get(shorturl=people_url)
    note = Note.objects.get(pk=note_url)
    notecomment = NoteComment.objects.filter(comment_note=note.id)

    content = {}

    follow = Friends.objects.filter(user=profile.user.id).order_by('created_time').reverse()
    follow_by = Friends.objects.filter(friend=profile.user.id).order_by('created_time').reverse()
    nav = navgation(request)
    content['nav'] = nav
    comment = NoteCommentForm()
    content['comment'] = comment
    content['notecomment'] = notecomment

    #渲染模板
    content['note'] = note
    content['follow'] = follow
    content['follow_by'] = follow_by
    content['profile'] = profile

    follow_btn = {}
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
    if note and profile:
        if request.method == 'GET':
            return render_to_response('note.html', {'content': content}, context_instance=RequestContext(request))

        elif request.method == 'POST':
            txt = request.POST.get("comment_content", '')
            comment = NoteComment()
            comment.comment_author = user
            comment.comment_note = note
            comment.comment_content = txt
            comment.comment_date = datetime.datetime.now()
            comment.save()

            notecomment = NoteComment.objects.filter(comment_note=note.id)
            content['notecomment'] = notecomment
            content['txt'] = txt
            return render_to_response('note.html', {'content': content}, context_instance=RequestContext(request))
    else:#404!!!
        return render_to_response('404.html', context_instance=RequestContext(request))


def notes(request, people_url):
    profile = Profile.objects.get(shorturl=people_url)
    note = Note.objects.filter(note_authors=profile.user.id)

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
            notes, page_range = paging(request, note, n)


            #渲染模板
            content['notes'] = notes
            content['follow'] = follow
            content['follow_by'] = follow_by
            content['profile'] = profile
            content['page_range'] = page_range

            follow_btn = {}
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
                    return render_to_response('note_list.html', {'content': content},
                                              context_instance=RequestContext(request))



            return render_to_response('note_list.html', {'content': content}, context_instance=RequestContext(request))
            #else:#404!!!
            #   return render_to_response('404.html',context_instance=RequestContext(request))
    else:#404!!!
        return render_to_response('404.html', context_instance=RequestContext(request))


@login_required()
def note_comment(request, people_url, note_url):
    note = Note.objects.get(pk=note_url)
    user = request.user

    if request.method == 'GET':
        comment = NoteComment.objects.filter(comment_note=note_url)
        content = {}
        content['comments'] = comment
        return render_to_response('note_comment_form.html', {'content': content},
                                  context_instance=RequestContext(request))


    elif request.method == 'POST':

        txt = request.POST.get("comment")
        comment = NoteComment()
        comment.comment_author = user
        comment.comment_note = note
        comment.comment_content = txt
        comment.comment_date = datetime.datetime.now()
        comment.save()

        response_data = {}
        response_data['comment'] = comment.comment_content
        response_data['comment_author_url'] = comment.comment_author.get_profile().shorturl
        response_data['comment_author_nickname'] = comment.comment_author.get_profile().nickname

        return HttpResponse(json.dumps(response_data), mimetype="application/json")






def note_del(request, people_url,note_url):
    note = Note.objects.get(pk=note_url)
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(shorturl=people_url)
    content = {}

    if note :
        if profile.user.id == user.id:
            nav = navgation(request)
            content['nav'] = nav

            if request.method == 'GET':
                n = 'note/%s/'%(note.id)


                status = Status.objects.get(status_url = n)
                status.delete()
                note.delete()
                return HttpResponseRedirect('http://localhost/people/%s/notes/' % people_url)
    else:
        return  render_to_response('note_list.html', {'content': content},context_instance=RequestContext(request))

