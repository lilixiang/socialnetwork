# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response
from socialnetwork.account.models import Profile
from socialnetwork.friend.models import Friends
from socialnetwork.status.models import Status
from socialnetwork.feed.views import paging

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User
from socialnetwork.feed.views import navgation
from socialnetwork.board.forms import BoardForm

import datetime


def people(request, people_url):
    profile = Profile.objects.get(shorturl=people_url)
    content = {}
    user_url = '/people/%s/' %request.user.get_profile().shorturl
    follow = Friends.objects.filter(user=profile.user.id).order_by('created_time').reverse()
    follow_by = Friends.objects.filter(friend=profile.user.id).order_by('created_time').reverse()

    feed = Status.objects.filter(status_author=profile.user.id)
    nav = navgation(request)
    content['nav'] = nav

    board = BoardForm(initial={'board_belong': '%s' % people_url})
    content['board'] = board
    content['user_url'] = user_url
    content['follow'] = follow
    content['follow_by'] = follow_by



    #分页使用
    n = 2
    feeds, page_range = paging(request, feed, n)


    #渲染模板
    content['feed'] = feeds
    content['page_range'] = page_range

    if profile:
        if request.method == 'GET':
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
                        return render_to_response('people.html', {'content': content},
                                                  context_instance=RequestContext(request))
                    else:
                        follow_btn['follow_url'] = 'http://localhost/people/%s/del' % people_url
                        follow_btn['type'] = u'取消关注'
                        return render_to_response('people.html', {'content': content},
                                                  context_instance=RequestContext(request))
                else:
                    follow_btn['type'] = None
                    return render_to_response('people.html', {'content': content},
                                              context_instance=RequestContext(request))
            else:
                return render_to_response('people.html', {'content': content}, context_instance=RequestContext(request))


        if request.method == 'POST':
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
                        return render_to_response('people.html', {'content': content},
                                                  context_instance=RequestContext(request))
                    else:
                        follow_btn['follow_url'] = 'http://localhost/people/%s/del' % people_url
                        follow_btn['type'] = u'取消关注'
                        return render_to_response('people.html', {'content': content},
                                                  context_instance=RequestContext(request))
                else:
                    follow_btn['type'] = None
                    form = BoardForm(request.POST.copy())
                    content['form'] = form
                    if form.is_valid():
                        if form.errors:
                            return render_to_response('people.html', {'content': content},
                                                      context_instance=RequestContext(request))
                        else:
                            now = datetime.datetime.now()
                            board = form.save(commit=False)
                            board.message_author = request.user
                            board.message_date = now
                            board.save()
                            return render_to_response('people.html', {'content': content},
                                                      context_instance=RequestContext(request))
                    return render_to_response('people.html', {'content': content},
                                              context_instance=RequestContext(request))


            return render_to_response('people.html', {'content': content}, context_instance=RequestContext(request))









def people_search(request):
    u = request.user.id
    profile = Profile.objects.get(user=u)
    content = {}
    user_url = '/people/%s/' %request.user.get_profile().shorturl
    follow = Friends.objects.filter(user=profile.user.id).order_by('created_time').reverse()
    follow_by = Friends.objects.filter(friend=profile.user.id).order_by('created_time').reverse()





    nav = navgation(request)
    content['nav'] = nav

    content['user_url'] = user_url
    content['follow'] = follow
    content['follow_by'] = follow_by


    if profile:
        if request.method == 'GET':
            s = request.GET.get('s')
            p = Profile.objects.filter(nickname__contains=s)
            follow_btn = {'follow_url': 'http://localhost/people/%s/add' %u, 'type': u'关注', }


            content['profile'] = profile
            content['follow_btn'] = follow_btn




            #分页使用
            n = 3
            profiles, page_range = paging(request, p, n)


            #渲染模板
            content['profiles'] = profiles
            content['page_range'] = page_range
            content['s'] = s


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
                        follow_btn['follow_url'] = 'http://localhost/people/%s/add' %u
                        follow_btn['type'] = u'关注'
                    else:
                        follow_btn['follow_url'] = 'http://localhost/people/%s/del' %u
                        follow_btn['type'] = u'取消关注'
                else:
                    follow_btn['type'] = None
                    return render_to_response('search.html', {'content': content},
                                              context_instance=RequestContext(request))
            else:
                return render_to_response('search.html', {'content': content}, context_instance=RequestContext(request))


@login_required()
def people_add(request, people_url):
    user = User.objects.get(pk=request.user.id)
    content = {}

    nav = navgation(request)
    content['nav'] = nav

    content['user'] = user
    content['people_url'] = people_url
    if people_url == user.id:
        return render_to_response('people.html', {'content': content}, context_instance=RequestContext(request))
    else:
        friend = Profile.objects.get(shorturl=people_url).user
        now = datetime.datetime.now()
    if request.method == 'GET':
        Friends(user=user, friend=friend, created_time=now).save()
        return HttpResponseRedirect('http://localhost/people/%s/' % people_url)


def people_del(request, people_url):
    user = User.objects.get(pk=request.user.id)
    content = {}
    nav = navgation(request)
    content['nav'] = nav

    content['user'] = user
    content['people_url'] = people_url
    if people_url == user.id:
        return render_to_response('people.html', {'content': content}, context_instance=RequestContext(request))
    else:
        friend = Profile.objects.get(shorturl=people_url).user
        if request.method == 'GET':
            f = Friends.objects.get(user=user, friend=friend)
            f.delete()
            return HttpResponseRedirect('http://localhost/people/%s/' % people_url)


def contact(request, people_url):
    profile = Profile.objects.get(shorturl=people_url)
    content = {}
    friend_url = '/people/%s/contact/list' %request.user.get_profile().shorturl
    follow = Friends.objects.filter(user=profile.user.id).order_by('created_time').reverse()
    follow_by = Friends.objects.filter(friend=profile.user.id).order_by('created_time').reverse()
    nav = navgation(request)
    content['nav'] = nav
    content['friend_url'] = friend_url



    #分页使用
    n = 2
    follows, page_range = paging(request, follow, n)


    #渲染模板
    content['follows'] = follows
    content['follow_by'] = follow_by
    content['profile'] = profile
    content['follow'] = follow

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
                return render_to_response('people_follow.html', {'content': content},
                                          context_instance=RequestContext(request))
            else:
                follow_btn['follow_url'] = 'http://localhost/people/%s/del' % people_url
                follow_btn['type'] = u'取消关注'
                return render_to_response('people_follow.html', {'content': content},
                                          context_instance=RequestContext(request))
        else:
            follow_btn['type'] = None
            return render_to_response('people_follow.html', {'content': content},
                                      context_instance=RequestContext(request))
    else:
        return render_to_response('people_follow.html', {'content': content}, context_instance=RequestContext(request))


def contact_r(request, people_url):
    profile = Profile.objects.get(shorturl=people_url)
    content = {}
    request_url = 'http://localhost/people/%s/' % people_url
    user_url = 'http://localhost/people/%d/' % request.user.id
    follow = Friends.objects.filter(user=profile.user.id).order_by('created_time').reverse()
    follow_by = Friends.objects.filter(friend=profile.user.id).order_by('created_time').reverse()
    nav = navgation(request)
    content['nav'] = nav
    content['user_url'] = user_url



    #分页使用
    n = 2
    follows, page_range = paging(request, follow_by, n)


    #渲染模板
    content['follows'] = follows
    content['follow_by'] = follow_by
    content['profile'] = profile
    content['follow'] = follow

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
                return render_to_response('people_follow_by.html', {'content': content},
                                          context_instance=RequestContext(request))
            else:
                follow_btn['follow_url'] = 'http://localhost/people/%s/del' % people_url
                follow_btn['type'] = u'取消关注'
                return render_to_response('people_follow_by.html', {'content': content},
                                          context_instance=RequestContext(request))
        else:
            follow_btn['type'] = None
            return render_to_response('people_follow_by.html', {'content': content},
                                      context_instance=RequestContext(request))
    else:
        return render_to_response('people_follow_by.html', {'content': content}, context_instance=RequestContext(request))
