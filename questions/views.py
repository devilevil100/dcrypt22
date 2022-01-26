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

# Create your views here.
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

        current.question = question

        current.save()
        check = CheckQues.objects.get(team=q, question=current.question)
        check.starttime =  datetime.datetime.now(datetime.timezone.utc)
        check.save()
        return render(request,"question.html", {"room": room.roomname})
    if not current.question:
        return redirect("dashboard:questions")

    return render(request,"question.html", {"question": current, "room": room.roomname})

@require_http_methods(["POST"])
def answer(request):
    if not request.session.get('name'):
        return redirect('dashboard:login')
    if 'team' in request.session.get('team'):
        return redirect('dashboard:dashboard')
    ans = request.POST.get('ans')
    name= request.session.get('name')[0]
    q = User.objects.get(p1name=name)
    current = CurrentQues.objects.get(team=q)

    special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if special_char.search(ans):

        return HttpResponse('hack')
    elif ans != current.question.answer:
        return HttpResponse('incorrect')
    else:
        check = CheckQues.objects.get(team=q, question=current.question)
        check.solved = True
        check.save()
        current.question = None
        check.endtime = datetime.datetime.now(datetime.timezone.utc)
        current.save()
        check.save()
        totaltimetaken = ((check.endtime - check.starttime).seconds % 3600) // 60
        point = Points.objects.get(user=q)
        point.flagpoints += 1000
        if totaltimetaken == 0:
            totaltimetaken = 1
        point.battlepoints += 1000 + round(100000/totaltimetaken)
        point.recentupdate = datetime.datetime.now(datetime.timezone.utc)
        point.save()

        request.session['correct'] = {'time':totaltimetaken, 'bp': 1000 + round(100000/totaltimetaken) }
        return HttpResponse('correct')
    return HttpResponse('')
