# Create your views here.
# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response
from socialnetwork.account.models import Profile
from socialnetwork.friend.models import Friends
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User
from socialnetwork.feed.views import navgation,paging
from socialnetwork.board.forms import BoardForm
from socialnetwork.board.models import Board

import datetime

def board(request,people_url):
    profile = Profile.objects.get(shorturl=people_url)
    content = {}
    request.path = '/people/%s/board/'%people_url

    nav = navgation(request)
    content['nav'] = nav

    board = BoardForm(initial={'board_belong': '%s'%people_url})
    content['board'] = board

    b = Board.objects.filter(board_belong=people_url).order_by('message_date').reverse()

    n = 2
    boards, page_range = paging(request, b, n)


    content['boards'] = boards
    content['page_range'] = page_range

    follow = Friends.objects.filter(user=profile.user.id).order_by('created_time').reverse()
    follow_by = Friends.objects.filter(friend=profile.user.id).order_by('created_time').reverse()
    nav = navgation(request)
    content['nav'] = nav

    #渲染模板
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

    if profile :
        if request.method == 'GET':
                return render_to_response('board.html', {'content': content},context_instance=RequestContext(request))
        if request.method == 'POST':
            form = BoardForm(request.POST.copy())
            content['form'] = form
            if form.is_valid() :
                if form.errors :
                    return render_to_response('board.html',{'content': content}, context_instance=RequestContext(request))
                else :
                    now = datetime.datetime.now()
                    board = form.save(commit = False)
                    board.message_author = request.user
                    board.message_date = now
                    board.save()
                    return render_to_response('board.html',{'content': content}, context_instance=RequestContext(request))
            return render_to_response('board.html', {'content': content},context_instance=RequestContext(request))
