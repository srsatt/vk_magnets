from django.shortcuts import render
from django import forms
from django.views.decorators.csrf import csrf_exempt
import json

import django_rq
from core import save_album

class NameForm(forms.Form):
    user_name = forms.CharField(label='vk.com', max_length=100)

def index(request):
    return render(request,'dashboard/index.html')

def friendspicker(request):
    return render(request,'dashboard/friendspicker.html')


@csrf_exempt
def receivefriends(request):
    friend_list = json.loads(request.body)
    print friend_list[0]
    django_rq.enqueue(save_album, friends=friend_list, user_id=42)
    return render(request,'dashboard/friendspicker.html')

def picker(request, id=''):
    context = {}
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            context = request_user_db_report(user_name)
    elif request.method == 'GET' and id:
        form = NameForm()
        user_name = id
        context = request_user_db_report(id)
    else:
        form = NameForm()
    context['form'] = form
    context['current_period_num'] = get_current_period_num()
    return render(request, 'dashboard/dossier.html', context)
