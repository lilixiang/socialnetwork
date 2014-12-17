# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response
from socialnetwork.status.forms import StatusForm
from socialnetwork.friend.models import Friends
from socialnetwork.account.models import Profile
from socialnetwork.status.models import Status

from socialnetwork.feed.models import Feed
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required()
def feed(request):
    user = request.user
    profile = Profile.objects.get(user=request.user.id)
    follow = Friends.objects.filter(user=user).order_by('created_time').reverse()
    follow_by = Friends.objects.filter(friend=user).order_by('created_time').reverse()

    feed = []

    nav = navgation(request)

    for f in follow :
        feed_update=Status.objects.filter(status_author=f.friend)
        feed += feed_update

    feed += Status.objects.filter(status_author=user.id)
    feed.sort(key=lambda object: object.status_date, reverse=True)


    status = StatusForm()


    #分页使用
    n = 5
    feeds,page_range = paging(request,feed,n)


    #渲染模板
    content = {}
    content['feed'] = feeds
    content['page_range'] = page_range

    content['nav'] = nav
    content['follow'] = follow.all()
    content['follow_by'] = follow_by.all()
    content['status'] = status
    content['profile'] = profile

    content['follow_by_url'] = 'http://localhost/people/%s/contact/rlist'%request.user.id
    content['note_url'] = 'http://localhost/people/%s/notes/'%request.user.id
    content['album_url'] = 'http://localhost/people/%s/albums/'%request.user.id
    content['status_url'] = 'http://localhost/people/%s/statuses/'%request.user.id


    if request.method == 'GET':

        return render_to_response('feed.html', {'content': content},context_instance=RequestContext(request))

    elif request.method == 'POST':


        form = StatusForm(request.POST.copy())
        content['form'] = form
        if form.errors :
           return render_to_response('status_form.html',{'content': content}, context_instance=RequestContext(request))
        else :
            now = datetime.datetime.now()
            status = form.save(commit = False)
            status.status_author = request.user
            status.status_type = u'Status'
            status.status_date = now
            status.save()
            s = Status.objects.get(pk=status.id)
            s.status_url = 'status/%s/'%(s.id)
            s.save()
            return HttpResponseRedirect('http://localhost/')
    else:
        return render_to_response('feed.html', {'content': content},context_instance=RequestContext(request))







def navgation(request):
    nav = {}
    nav['home'] = 'http://localhost'
    nav['ihome'] = 'http://localhost/people/%s/'%request.user.get_profile().shorturl
    nav['friend'] = 'http://localhost/people/%s/contact/list'%request.user.get_profile().shorturl
    nav['account'] = 'http://localhost/account/'
    nav['logout'] = 'http://localhost/account/logout'
    return nav


def paging(request,object,num):
    paginator = Paginator(object, num) # Show 2 contacts per page

    page = request.GET.get('page')
    if page < 1:
        page=1

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objects = paginator.page(paginator.num_pages)

    after_range_num = 5
    bevor_range_num = 5
    if int(page) >=  after_range_num:
        page_range = objects.paginator.page_range[int(page)-after_range_num:int(page)+bevor_range_num]

    else:
        page_range = objects.paginator.page_range[0:10]


    return objects,page_range