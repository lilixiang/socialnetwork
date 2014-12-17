# -*- coding: utf-8 -*-

# Create your views here.
from django.shortcuts import render_to_response
from socialnetwork.status.models import Status,Comment
from socialnetwork.status.forms import StatusForm,CommentForm
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from socialnetwork.feed.views import navgation

import datetime,json



@login_required()
def status_create(request,people_url):
    user = request.user.id
    content = {}

    nav = navgation(request)
    content['nav'] = nav
    if request.method == 'GET':
        form = StatusForm()
        content['form'] = form
        return render_to_response('status_form.html',{'content': content}, context_instance=RequestContext(request))
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
            s.status_url = 'http://localhost/people/%s/status/%s/'%(people_url, s.id)
            s.save()
            return HttpResponseRedirect('http://localhost/people/%s/status/%s/'%(people_url, s.id))
    return render_to_response('status_form.html',{'content': content}, context_instance=RequestContext(request))



def status(request,people_url,status_url):
    status = Status.objects.get(id=status_url)
    comment = Comment.objects.filter(comment_status=status.id)
    reply = {'reply_url':'/people/%s/status/%s/'%(people_url, status_url),'name':u'回应',}
    content ={}

    nav = navgation(request)
    content['nav'] = nav


    content['status'] = status
    content['comment'] = comment
    content['reply'] = reply
    if  status :
        if request.method == 'GET':
            return render_to_response('status.html', {'content': content}, context_instance=RequestContext(request))
        if request.method == 'POST':
            return render_to_response('status.html', {'content': content}, context_instance=RequestContext(request))
    return render_to_response('status.html',{'content': content}, context_instance=RequestContext(request))




@login_required()
def status_comment(request,people_url,status_url):
    status = Status.objects.get(id=status_url)
    user = request.user


    if request.method == 'GET':
        comment = Comment.objects.filter(comment_status=status_url)
        content = {}
        nav = navgation(request)
        content['nav'] = nav
        content['comments'] = comment


        return render_to_response('status_comment_form.html',{'content': content}, context_instance=RequestContext(request))


    elif request.method == 'POST':

        txt = request.POST.get("comment")
        comment = Comment()
        comment.comment_author = user
        comment.comment_status = status
        comment.comment_content = txt
        comment.comment_date = datetime.datetime.now()
        comment.save()

        response_data= {}
        response_data['comment'] = comment.comment_content
        response_data['comment_author_url'] = comment.comment_author.get_profile().shorturl
        response_data['comment_author_nickname'] = comment.comment_author.get_profile().nickname

        return HttpResponse(json.dumps(response_data), mimetype="application/json")


