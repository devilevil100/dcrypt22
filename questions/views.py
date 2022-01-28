from django.shortcuts import render
from django.shortcuts import render, redirect
import gspread
from django.http import HttpResponse
import time
import re
from users.models import User, Points, Room
from questions.models import Question, CheckQues, CurrentQues
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.http import require_http_methods
import datetime

from ratelimit.decorators import ratelimit
import requests
from discord import Webhook, RequestsWebhookAdapter

hacweb = Webhook.from_url("https://discord.com/api/webhooks/936104524630859826/qtxMSv9v5namavQoOU9mrrHVt4r4UKpNzcRGTfH8JiU7hJNeMD53dbwMpTyV8aRStdJ9", adapter=RequestsWebhookAdapter())
solveweb = Webhook.from_url("https://discord.com/api/webhooks/936104431710240778/k2cWCESgnPYD5trvW-NvRgGa39Qt5L47Pvv_bJs2fNW4ZJsXChuvoZOE8_5vRvg30tKi", adapter=RequestsWebhookAdapter())



@ratelimit(key='ip', rate='5/m')
def quest(request):
    if not request.session.get('name'):
        return redirect('dashboard:login')
    if 'team' in request.session.get('team'):
        return redirect('dashboard:dashboard')
   
    name= request.session.get('name')[0]
    q = User.objects.get(p1name=name)
    room = Room.objects.get(user=q)

    current = CurrentQues.objects.get(team=q)

    if request.method == "POST":
        questioncontext = request.POST.get('ques')
        question = Question.objects.get(heading=questioncontext)
        current = CurrentQues.objects.get(team=q)
        if current.question:
            return redirect("questions:quest")
        current.question = question

        current.save()
        check = CheckQues.objects.get(team=q, question=current.question)
        check.starttime =  datetime.datetime.now(datetime.timezone.utc)
        check.save()
        return render(request,"question.html", {"room": room.roomname})
    if not current.question:
        return redirect("dashboard:questions")
    incorr = "no"
    if request.session.get('incorrect'):
        incorr = "yes"
        request.session.pop('incorrect')
    hacc = "no"
    if request.session.get('hack'):
        hacc = "yes"
        request.session.pop('hack')
    return render(request,"question.html", {"question": current, "room": room.roomname, "incor":incorr, "hacc":hacc})


@ratelimit(key='ip', rate='5/m')
@require_http_methods(["POST"])
def answer(request):
    if not request.session.get('name'):
        return redirect('dashboard:login')
    if 'team' in request.session.get('team'):
        return redirect('dashboard:dashboard')
    ans = request.POST.get('ans').replace(" ","").lower()
    name= request.session.get('name')[0]
    q = User.objects.get(p1name=name)
    current = CurrentQues.objects.get(team=q)

    special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if special_char.search(ans):
        hacweb.send(f"{q.teamname} typed {ans} thus using special chars in {current.question.heading}")
        request.session['hack'] = "yes"
        return HttpResponse('reload')
    elif ans != current.question.answer:
        request.session['incorrect'] = "yes"
        return HttpResponse('reload')
    else:
        check = CheckQues.objects.get(team=q, question=current.question)
        check.solved = True
        check.save()
        awardedbp = current.question.bp
        heading = current.question.heading
       
                   
        current.question = None
        check.endtime = datetime.datetime.now(datetime.timezone.utc)
        current.save()
        check.save()
        totaltimetaken = ((check.endtime - check.starttime).seconds) // 60
        point = Points.objects.get(user=q)
        point.flagpoints += 1000
        if totaltimetaken == 0:
            totaltimetaken = 1
        point.battlepoints += awardedbp
        point.recentupdate = datetime.datetime.now(datetime.timezone.utc)
        point.save()
        solveweb.send(f"{q.teamname} has solved {heading} got {awardedbp} BP")
        request.session['correct'] = {'time':totaltimetaken, 'bp': awardedbp  }
        return HttpResponse('correct')
    

