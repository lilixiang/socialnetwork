# -*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib import auth
from socialnetwork.account.forms import RegisterForm, LoginForm, ProfileForm
from socialnetwork.account.models import Profile
from socialnetwork.friend.models import Friends
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import datetime,time,random,base64,os
from socialnetwork.feed.views import navgation
from  django.core.files import File





@login_required()
def account(request):
    user = User.objects.get(pk=request.user.id)
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
        form = ProfileForm(instance=user.get_profile())
        content['form'] = form
        return render_to_response('account.html', {'content': content}, context_instance=RequestContext(request))
    elif request.method == 'POST':
        form = ProfileForm(request.POST, instance=user.get_profile())
        content['form'] = form
        if form.is_valid():
            if form.errors:
                return render_to_response('account.html', {'content': content},
                                          context_instance=RequestContext(request))
            else:
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                return HttpResponseRedirect('/account/')
        return render_to_response('account.html', {'content': content}, context_instance=RequestContext(request))


def login(request):
    if not request.user.is_authenticated():
        if request.method == 'POST':
            form = LoginForm(request.POST.copy())
            content = {'form': form, 'title': u'登录', }
            if form.is_valid():
                form = form.auth_user()
                if form.errors:
                    content['form'] = form
                    return render_to_response('login.html', {'content': content},
                                              context_instance=RequestContext(request))
                else:
                    username = form.cleaned_data.get('username')
                    password = form.cleaned_data.get('password')
                    user = auth.authenticate(username=username, password=password)
                    auth.login(request, user)
                    request.session['username'] = username
                    return HttpResponseRedirect('http://localhost/')
            else:
                return render_to_response('login.html', {'content': content}, context_instance=RequestContext(request))
        elif request.method == 'GET':
            form = LoginForm()
            content = {'form': form, 'title': u'登录', }
            return render_to_response('login.html', {'content': content}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('http://localhost/account/login/')


def register(request):
    if request.method == 'POST':
        content = {}

        form = RegisterForm(request.POST.copy())
        content['form'] = form

        if form.is_valid():
            form = form.auth_user()
            form = form.auth_email()
            if form.errors:
                return render_to_response('register.html', {'content': content},
                                          context_instance=RequestContext(request))
            else:
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                password_confirm = form.cleaned_data.get('password_confirm')
                if password == password_confirm:
                    email = form.cleaned_data.get('email')
                    user = User.objects.create_user(username=username,
                                                    password=password,
                                                    email=email
                    )
                    user.save()
                    user = auth.authenticate(username=username, password=password)
                    auth.login(request, user)
                    return HttpResponseRedirect('http://localhost/account/')
                else:
                    form._errors["username"] = form.error_class([u'两次密码不一致！'])
                    return render_to_response('register.html', {'content': content},
                                              context_instance=RequestContext(request))

        else:
            return render_to_response('register.html', {'content': content}, context_instance=RequestContext(request))

    else:
        form = RegisterForm()
        content = {'form': form}
        return render_to_response('register.html', {'content': content}, context_instance=RequestContext(request))






@login_required()
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/account/login/')



@login_required()
def user_icon(request):

    profile = Profile.objects.get(user=request.user.id)
    uid = str(request.user.id)
    path = 'http://localhost/static/avatar/'
    upload_path = 'http://localhost/media/avatar/'




    swfObj = ('<object name="c_avatar" type="application/x-shockwave-flash" width="720" height="420" '
                'id="c_avatar_miniblog1" align="middle" data="'+path+'c_avatar.swf">'
                '<param name="allowScriptAccess" value="always" />'
                '<param name="allowfullscreen" value="true" />'
	            '<param name="AllowNetworking" value="all" />'
	            '<param name="quality" value="high" />'
	            '<param name="bgcolor" value="#ffffff" />'
	            '<param name="menu" value="false" />'
	            '<param name="flashvars" value="big_avatar_url='+profile.avatar_big.url+'&middle_avatar_url='+ profile.avatar_middle.url +'&little_avatar_url='+ profile.avatar_little.url+'&big_avatar_name='+ uid +'_big&middle_avatar_name='+ uid +'_middle&little_avatar_name='+ uid +'_little&url_params=" />'
	            '</object>')




    user = User.objects.get(pk=request.user.id)
    content = {}

    nav = navgation(request)
    content['nav'] = nav
    content['swf'] = swfObj

    if request.method == 'GET':

        return render_to_response('user-icon.html', {'content': content}, context_instance=RequestContext(request))
    elif request.method == 'POST':

        img_type = str(request.POST.get('image_type'))

        r = random.randint(1, 1000)
        filename_big = '%s_big_%s%s'%(uid,r,img_type)
        filename_middle = '%s_middle_%s%s'%(uid,r,img_type)
        filename_little = '%s_little_%s%s'%(uid,r,img_type)

        data_big = base64.b64decode(request.POST['big_avatar'])
        data_middle = base64.b64decode(request.POST['middle_avatar'])
        data_little = base64.b64decode(request.POST['little_avatar'])


        out_big = open('E:/www/socialnetwork/temp/'+filename_big,'wb')
        out_big.write(data_big)
        out_big.close()

        out_middle = open('E:/www/socialnetwork/temp/'+filename_middle,'wb')
        out_middle.write(data_middle)
        out_middle.close()

        out_little = open('E:/www/socialnetwork/temp/'+filename_little,'wb')
        out_little.write(data_little)
        out_little.close()


        f_big = open('E:/www/socialnetwork/temp/'+filename_big,'rb')
        profile.avatar_big.save(filename_big,File(f_big))
        f_big.close()

        f_middle = open('E:/www/socialnetwork/temp/'+filename_middle,'rb')
        profile.avatar_middle.save(filename_middle,File(f_middle))
        f_middle.close()

        f_little = open('E:/www/socialnetwork/temp/'+filename_little,'rb')
        profile.avatar_little.save(filename_little,File(f_little))
        f_little.close()

        os.remove('E:/www/socialnetwork/temp/'+filename_big)
        os.remove('E:/www/socialnetwork/temp/'+filename_middle)
        os.remove('E:/www/socialnetwork/temp/'+filename_little)

        return HttpResponse('200')

