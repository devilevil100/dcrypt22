from django.shortcuts import render, redirect
import gspread
import time
from users.models import User, Points, Troops, Cooldown, PowerUp, HourlyFp, Room, Notif
from questions.models import Question, CheckQues, CurrentQues
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.http import require_http_methods
import re
from django.http import HttpResponse
import threading
import datetime
import string
import random
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
N = 7
import requests
from discord import Webhook, RequestsWebhookAdapter

hacweb = Webhook.from_url("https://discord.com/api/webhooks/936104524630859826/qtxMSv9v5namavQoOU9mrrHVt4r4UKpNzcRGTfH8JiU7hJNeMD53dbwMpTyV8aRStdJ9", adapter=RequestsWebhookAdapter())
solveweb = Webhook.from_url("https://discord.com/api/webhooks/936104431710240778/k2cWCESgnPYD5trvW-NvRgGa39Qt5L47Pvv_bJs2fNW4ZJsXChuvoZOE8_5vRvg30tKi", adapter=RequestsWebhookAdapter())
attacweb = Webhook.from_url("https://discord.com/api/webhooks/936109964366319616/ex8cmYSpBJi5wtmxltNB-Z_m0hlovhArPyUutfXpnxWWWLuc3w9Nhj0v8zKnX5WkjTHw", adapter=RequestsWebhookAdapter())
notifyweb = Webhook.from_url("https://discord.com/api/webhooks/936110900732125204/TN8g4Oq855W9FA3G4vqIIea2gcNPMzPTgbyFEh_DP3Pr6g7ExAaBW1no510-CSpMA6K1", adapter=RequestsWebhookAdapter())
def hourlyfp():
    while True:
        hourlyfp = HourlyFp.objects.all()
        for user in hourlyfp:
            if user.recent:
                if user.recent +datetime.timedelta(hours=1) <= datetime.datetime.now(datetime.timezone.utc):
                    p = Points.objects.get(user=user.user)
                    if user.poisoned:
                        if user.poisonedtill > datetime.datetime.now(datetime.timezone.utc):
                            continue
                        elif user.poisonedtill <= datetime.datetime.now(datetime.timezone.utc):
                            user.poisoned = False
                    if user.bonusfp:
                        if user.bonustill <= datetime.datetime.now(datetime.timezone.utc):
                            bonusfp = "no"
                            user.bonusfp = False
                        else:
                            bonusfp = "yes"
                    else:
                        bonusfp = "no"
                    if  bonusfp == "yes":
                        p.flagpoints += 400
                    elif bonusfp == "no":
                        p.flagpoints += 200
                    p.save()
                    user.recent = datetime.datetime.now(datetime.timezone.utc)
                    user.save()
            else:
                p = Points.objects.get(user=user.user)
                if user.poisoned:
                    if user.poisonedtill > datetime.datetime.now(datetime.timezone.utc):
                        continue
                if user.bonusfp:
                    if user.bonustill <= datetime.datetime.now(datetime.timezone.utc):
                        bonusfp = "no"
                    else:
                        bonusfp = "yes"
                else:
                    bonusfp = "no"
                if  bonusfp == "yes":
                    p.flagpoints += 220
                elif bonusfp == "no":
                    p.flagpoints += 200
                p.save()
                user.recent = datetime.datetime.now(datetime.timezone.utc)
                user.save()
        time.sleep(1)
t = threading.Thread(target=hourlyfp)
t.setDaemon(True)
t.start()
for user in User.objects.all():
    if not Room.objects.filter(user=user).exists():
        f = Room(user=user, roomname=''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k = N)))
        f.save()
def index(request):
    if request.session.has_key('team'):
        return redirect("dashboard:dashboard")
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(p1email=email):
            q= User.objects.get(p1email=email)
            if check_password(password, q.password):
                request.session['team'] =q.teamname
                request.session["participant"] = 1
                if q.p2name != " NA " and q.p3name != " NA ":
                    request.session['name'] = [q.p1name, q.p2name, q.p3name]
                elif q.p2name !=" NA " and q.p3name == " NA ":
                    request.session['name'] = [q.p1name, q.p2name]
                else:
                    request.session['name'] = [q.p1name]
                request.session['email'] =email
                return redirect("dashboard:dashboard")
            else:
                return render(request,"login.html", {"error": "Password is incorrect "})
        elif User.objects.filter(p2email=email):
            q= User.objects.get(p2email=email)
            if check_password(password, q.password):
                request.session['team'] =q.teamname
                request.session["participant"] = 2
                if q.p2name != " NA " and q.p3name != " NA ":
                    request.session['name'] = [q.p1name, q.p2name, q.p3name]
                elif q.p2name !=" NA " and q.p3name == " NA ":
                    request.session['name'] = [q.p1name, q.p2name]
                else:
                    request.session['name'] = [q.p1name]
                request.session['email'] =email
                return redirect("dashboard:dashboard")
            else:
                return render(request,"login.html", {"error": "Password is incorrect "})
        elif User.objects.filter(p3email=email):
            q= User.objects.get(p3email=email)
            if check_password(password, q.password):
                request.session['team'] =q.teamname
                request.session["participant"] = 3
                if q.p2name != " NA " and q.p3name != " NA ":
                    request.session['name'] = [q.p1name, q.p2name, q.p3name]
                elif q.p2name !=" NA " and q.p3name == " NA ":
                    request.session['name'] = [q.p1name, q.p2name]
                else:
                    request.session['name'] = [q.p1name]
                request.session['email'] =email
                return redirect("dashboard:dashboard")
            else:
                return render(request,"login.html", {"error": "Password is incorrect "})
        else:
            return render(request,"login.html", {"error": "Email Or Password is incorrect "})
    return render(request,"login.html")

def dashboard(request):
    print(request.session.get('team'))

    if request.method == "POST":
        teamname = request.POST.get('teamname')
        if teamname == "NA" or 'team' in teamname:
            request.session['error'] = "teamname cant have team in it or be NA"
            return redirect("dashboard:dashboard")
        password = request.POST.get('password')
        email = request.session.get('email')
        if User.objects.filter(p1email=email):
            q= User.objects.get(p1email=email)
            q.teamname = teamname.replace(" ","")
            request.session['team'] =teamname
            q.password = make_password(password)
            q.save()
        elif User.objects.filter(p2email=email):
            q= User.objects.get(p2email=email)
            q.teamname = teamname.replace(" ","")
            request.session['team'] =teamname
            q.password = make_password(password)
            q.save()
        elif User.objects.filter(p3email=email):
            q= User.objects.get(p3email=email)
            q.teamname = teamname.replace(" ","")
            request.session['team'] =teamname
            q.password = make_password(password)
            q.save()
        return redirect("dashboard:dashboard")
    if not request.session.has_key('team'):
        return redirect("dashboard:login")
    team = request.session.get('team')
    name= request.session.get('name')[0]
    q = User.objects.get(p1name=name)
    points = Points.objects.get(user=q)
    troops = Troops.objects.get(user=q)
    shield = Cooldown.objects.get(user=q).shield
    if shield:
        if datetime.datetime.now(datetime.timezone.utc) < shield:
            shieldduration = (shield - datetime.datetime.now(datetime.timezone.utc)).seconds
        else:
            shieldduration = 0
    else:
        shieldduration = 0
    attack = Cooldown.objects.get(user=q).attack
    if attack:
        if datetime.datetime.now(datetime.timezone.utc) < attack:
            attackcooldown = (attack - datetime.datetime.now(datetime.timezone.utc) ).seconds
        else:
            attackcooldown = 0
    else:
        attackcooldown = 0
    hfp = HourlyFp.objects.get(user=q)
    if hfp.poisoned:
        poisoned= "yes"
    else:
        poisoned = "no"
    if hfp.bonusfp:
        bonusfp = "yes"
    else:
        bonusfp = "no"
    room = Room.objects.get(user=q)
    notifs = Notif.objects.filter(room=room)
    def Reverse(lst):
        return [ele for ele in reversed(lst)]
    error = "no"
    if request.session.get('error'):
        error = request.session.get('error')
    powerups = PowerUp.objects.get(user=q)
    points.defensepoints = troops.soldiers*100 + troops.tanks*350 + troops.aag*300
    points.save()
    return render(request,"dashboard.html", {"name": ','.join(request.session.get('name')), "team": team, "flagp": points.flagpoints, "battlep": points.battlepoints, "defensep": points.defensepoints, "troops": troops, "shield": shieldduration, "attack":attackcooldown, "poisoned": poisoned, "bonus": bonusfp, "room": room.roomname, "notifs": Reverse(notifs), "error":error, "powerups": {"multi": powerups.multiplier, "hp": powerups.hp, "poison": powerups.poison},  "dp": points.defensepoints})

def leaderboard(request):
    if not request.session.get('name'):
        return redirect('dashboard:login')
    if 'team' in request.session.get('team'):
        return redirect('dashboard:dashboard')
    dataset = []
    points = Points.objects.filter().order_by('-flagpoints', 'recentupdate')
    name= request.session.get('name')[0]
    q = User.objects.get(p1name=name)
    powerups = PowerUp.objects.get(user=q)
    poisoned = "no"
    if request.session.get('poison'):
        poisoned = request.session.get('poison')
        request.session.pop('poison')
    troops = Troops.objects.get(user=q)
    attackcool = Cooldown.objects.get(user=q).attack

    if attackcool:
        if attackcool < datetime.datetime.now(datetime.timezone.utc):
            if troops.soldiers == 0 and troops.tanks == 0 and troops.bombers == 0:
                attack = "no"
            else:
                attack = "yes"
        else:
            attack = "no"
    else:
        if troops.soldiers == 0 and troops.tanks == 0 and troops.bombers == 0:
            attack = "no"
        else:
            attack = "yes"
    poison = "no"
    room = Room.objects.get(user=q)


    for p in points:
        if p.user == q:
            dataset.append({"teamname": p.user.teamname, "flagp": p.flagpoints, "attackpossible": "no", "poison":"no", "poisoned": poisoned, "p1name": p.user.p1name, "room": room.roomname  })
            continue
        cooldown = Cooldown.objects.get(user=p.user)


        if powerups.poison > 0:

            hfp = HourlyFp.objects.get(user=p.user)
            if not hfp.poisoned:
                poison = "yes"
        if cooldown.shield:
            if cooldown.shield < datetime.datetime.now(datetime.timezone.utc):

                dataset.append({"teamname": p.user.teamname, "flagp": p.flagpoints, "attackpossible": "yes", "poison": poison, "poisoned": poisoned, "p1name": p.user.p1name, "room": room.roomname  })
            else:
                dataset.append({"teamname": p.user.teamname, "flagp": p.flagpoints, "attackpossible": "no", "poison": poison, "poisoned": poisoned, "p1name": p.user.p1name, "room": room.roomname  })
        else:
            dataset.append({"teamname": p.user.teamname, "flagp": p.flagpoints, "attackpossible": "yes", "poison": poison, "poisoned": poisoned, "p1name": p.user.p1name, "room": room.roomname  })
    multiplier = "no"
    status = "no"
    if powerups.multiplier > 0:
        multiplier = powerups.multiplier
    if attack == "no":
        for data in dataset:
            data['attackpossible'] = "no"
    if request.session.get('status'):
        status = request.session.get('status')
        request.session.pop('status')
    return render(request,"leaderboard.html", {"points": dataset, "attack": attack, "troops": troops, "multiplier":multiplier, "poison":poison, "poisoned": poisoned, "room": room.roomname, "status": status   })

def shop(request):
    if not request.session.get('name'):
        return redirect('dashboard:login')
    if 'team' in request.session.get('team'):
        return redirect('dashboard:dashboard')
    name= request.session.get('name')[0]
    q = User.objects.get(p1name=name)
    points = Points.objects.get(user=q)
    cool = Cooldown.objects.get(user=q)
    if cool.shield:
        if cool.shield > datetime.datetime.now(datetime.timezone.utc):
            shield="no"
        elif cool.shield < datetime.datetime.now(datetime.timezone.utc):
            shield = "yes"
    else:
        shield = "yes"
    powerup = PowerUp.objects.get(user=q)
    if powerup.hp > 0:
        hp = "yes"
    else:
        hp = "no"
    hfp = HourlyFp.objects.get(user=q)
    if hfp.bonusfp:
        bonusfp = "no"
    else:
        bonusfp = "yes"
    boughtitems = "no"
    if request.session.get('bought'):
        boughtitems = request.session.get('bought')
        request.session.pop('bought')
    room = Room.objects.get(user=q)
    return render(request,"shop.html", {"points": points,"battlep": points.battlepoints, "shield":shield,  "hp":hp , "bonusfp": bonusfp, "boughtitems": boughtitems, "room": room.roomname})

@require_http_methods(["POST"])
def buytroops(request):
    if not request.session.get('name'):
        return redirect('dashboard:login')
    if 'team' in request.session.get('team'):
        return redirect('dashboard:dashboard')
    soldiers = int(request.POST.get('soldiers'))
    bombers = int(request.POST.get('bombers'))
    tanks = int(request.POST.get('tanks'))
    aag = int(request.POST.get('aag'))
    multiplier = int(request.POST.get('multiplier'))
    shield = int(request.POST.get('shield'))
    hp = int(request.POST.get('hp'))
    poison = int(request.POST.get('poison'))
    bonusfp = int(request.POST.get('bonusfp'))
    special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if soldiers < 0 or bombers < 0 or tanks < 0 or aag <0 or multiplier < 0 or shield < 0 or hp < 0 or poison < 0 or bonusfp <0 :
        hacweb.send(f"{request.session.get('name')[0]} changed input value of troops or powerups in shop")
        return HttpResponse('hack')
    name= request.session.get('name')[0]
    q = User.objects.get(p1name=name)
    points = Points.objects.get(user=q)
    troops = Troops.objects.get(user=q)
    powerup = PowerUp.objects.get(user=q)
    cool = Cooldown.objects.get(user=q)
    if shield >1:
        hacweb.send(f"{q.teamname} tried to get shield tho they had a shield")
        return HttpResponse('hack')
    if shield > 0:
        if cool.shield:
            if cool.shield > datetime.datetime.now(datetime.timezone.utc):
                hacweb.send(f"{q.teamname} tried to get shield tho they had a shield")
                return HttpResponse('hack')
            else:
                cool.shield = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        else:
            cool.shield = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        cool.save()
    if powerup.hp > 0:
        totalcost = soldiers*50 + bombers*120 + tanks*200 + aag*125 + multiplier*2500 + shield*2500 + hp*2500 + poison*3000 + bonusfp*3000
        
        powerup.hp = 0
        powerup.save()
        room2 = Room.objects.get(user=q)
        newnotif = Notif(user=room2.user, room=room2, context=f"You used up the Half Price." )
        newnotif.save()
    else:
        totalcost = soldiers*100 + bombers*250 + tanks*400 + aag*250 + multiplier*2500 + shield*2500 + hp*2500 + poison*3000 + bonusfp*3000
    if totalcost > points.battlepoints:
        hacweb.send(f"{q.teamname} changed cost of troops or powerups in shop. totalcost was {totalcost} BP and totalbp was {points.battlepoints} BP")
        return HttpResponse('hack')
    troops.soldiers += soldiers
    troops.bombers += bombers
    troops.tanks += tanks
    troops.aag += aag

    troops.save()
    powerup.multiplier += multiplier
    powerup.poison += poison
    powerup.hp += hp
    hfp = HourlyFp.objects.get(user=q)
    if bonusfp >0:
        if hfp.bonusfp:
            hacweb.send(f"{q.teamname} took bonusfp even tho they had ongoing bonusfp")
            return HttpResponse('hack')
        hfp.bonusfp = True
        hfp.bonustill = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=5)
        hfp.save()
    powerup.save()

    points.battlepoints -= totalcost
    points.defensepoints +=  soldiers*100 + + tanks*350 + aag*300
    points.save()
    request.session["bought"] = totalcost
    print(soldiers, bombers, tanks, aag)
    return HttpResponse('bought')

@require_http_methods(["POST"])
def attack(request):
    if not request.session.get('name'):
        return redirect('dashboard:login')
    if 'team' in request.session.get('team'):
        return redirect('dashboard:dashboard')
    name= request.session.get('name')[0]
    q = User.objects.get(p1name=name)
    usercool = Cooldown.objects.get(user=q)
    if usercool.attack:
        if usercool.attack > datetime.datetime.now(datetime.timezone.utc):
            hacweb.send(f"{q.teamname} tried to attack tho they have an attack cooldown.")
            return HttpResponse('hack')
    soldiers = int(request.POST.get('soldiers'))
    tanks = int(request.POST.get('tanks'))
    bombers = int(request.POST.get('bombers'))
    team = request.POST.get('team')
    if soldiers < 0 or tanks < 0 or bombers <0 :
        hacweb.send(f"{q.teamname} tried to send negative troops to attack.")
        return HttpResponse('hack')
    name= request.session.get('name')[0]
    q = User.objects.get(p1name=name)
    points = Points.objects.get(user=q)
    troops = Troops.objects.get(user=q)
    if soldiers > troops.soldiers or tanks > troops.tanks or bombers > troops.bombers:
        hacweb.send(f"{q.teamname} tried to attack with troops greater than they have.")
        return HttpResponse('hack')
    attackedteam = User.objects.get(teamname=team)

    if attackedteam:
        cool = Cooldown.objects.get(user=attackedteam)
        if cool.shield:
            if cool.shield > datetime.datetime.now(datetime.timezone.utc):
                hacweb.send(f"{q.teamname} tried to attack {attackedteam.teamname} tho they had shield.")
                return HttpResponse('hack')

    else:
        hacweb.send("{q.teamname} tried to attack null team.")
        return HttpResponse('hack')
    victimtroops = Troops.objects.get(user=attackedteam)
    
    
    attackpoints = 100*soldiers + 350*bombers + 500*tanks
    multiplier = request.POST.get('multi')
    if multiplier == "yes":
        attackpoints = attackpoints*1.5
        powerup = PowerUp.objects.get(user=q)
        powerup.multiplier -= 1
        powerup.save()
    victimpoints = Points.objects.get(user=attackedteam)
    status = "null"
    troops.soldiers -= soldiers
    troops.bombers -= bombers
    troops.tanks -= tanks
    troops.save()
    defensewalesoldiers = victimtroops.soldiers
    defensewaletanks = victimtroops.tanks
    defensewaleaag = victimtroops.aag
    attacksepehledp = victimpoints.defensepoints
    print(attackpoints)
    if usercool.shield:
        usercool.shield = None
    if attackpoints > victimpoints.defensepoints:
        status = "win"
        points.flagpoints += round((victimpoints.flagpoints)/2)
        points.defensepoints -= soldiers*100 + tanks*350
        wonpoints = round((victimpoints.flagpoints)/2)
        victimpoints.flagpoints -= round((victimpoints.flagpoints)/2)
        points.save()
        victimpoints.save()
        victimtroops.soldiers = 0
        victimtroops.bombers = 0
        victimtroops.tanks = 0
        victimtroops.aag = 0
        victimtroops.save()
        victimpoints.defensepoints = 0
        victimpoints.save()
    elif attackpoints <= victimpoints.defensepoints:
        status = "lose"
        
        victimpoints.flagpoints += round((points.flagpoints)/4)
        lostpoints = round((points.flagpoints)/4)
        points.flagpoints -= round((points.flagpoints)/4)
        points.defensepoints -= soldiers*100 + tanks*350
        points.save()
        victimpoints.save()
        victimtroops.soldiers = 0
        victimtroops.bombers = 0
        victimtroops.tanks = 0
        victimtroops.aag = 0
        print( victimpoints.defensepoints - attackpoints)
        lefttroops = round(( victimpoints.defensepoints - attackpoints)/100)
        victimtroops.soldiers = lefttroops
        victimtroops.save()
        victimpoints.defensepoints = 100*lefttroops
        victimpoints.save()
    usercool.attack = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=10)
    cool = Cooldown.objects.get(user=attackedteam)
    cool.shield = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)
    usercool.save()
    cool.save()
    room = Room.objects.get(user=attackedteam)
    if status == "win":
        attacweb.send(f"{q.teamname} {attackpoints} AP - {soldiers} S| {tanks} T| {bombers} B  attacked {attackedteam.teamname} {attacksepehledp} DP - {defensewalesoldiers} S| {defensewaletanks} T| {defensewaleaag} A| and gained {wonpoints} FP")
        if attackedteam.p2discord:
            p2discord = attackedteam.p2discord
        else:
            p2discord = "NA"
        if attackedteam.p3discord:
            p3discord = attackedteam.p3discord
        else:
            p3discord = "NA"
        notifyweb.send(f"{attackedteam.p1discord}, {p2discord}, {p3discord}, Master! You were attacked and you lost {wonpoints} FP")
        request.session['status'] = {"status":"win", "flagp":wonpoints }
        room2 = Room.objects.get(user=q)
        newnotif = Notif(user=room2.user, room=room2, context=f"You won the attack on {attackedteam.teamname} and were awarded with {wonpoints} FP" )
        newnotif.save()
    
        notifattacked = Notif(user=room.user, room=room, context=f'Somebody attacked and you lost! {wonpoints} flagpoints were taken from you. ')
        notifattacked.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            room.roomname,
            {
                'type': 'chat_message',
                'status': 'lose',
                'message': f'Somebody attacked and you lost! {wonpoints} flagpoints were taken from you. '
            }
        )
    elif status == "lose":
        attacweb.send(f"{q.teamname} {attackpoints} AP - {soldiers} S| {tanks} T| {bombers} B  attacked {attackedteam.teamname} {attacksepehledp} DP - {defensewalesoldiers} S| {defensewaletanks} T| {defensewaleaag} A| and lost {lostpoints} FP")
        if attackedteam.p2discord:
            p2discord = attackedteam.p2discord
        else:
            p2discord = "NA"
        if attackedteam.p3discord:
            p3discord = attackedteam.p3discord
        else:
            p3discord = "NA"
        notifyweb.send(f"{attackedteam.p1discord}, {p2discord}, {p3discord}, Master! You were attacked and you won {lostpoints} FP")
        request.session['status'] = {"status":"lose", "flagp":lostpoints }
        room2 = Room.objects.get(user=q)
        newnotif = Notif(user=room2.user, room=room2, context=f"You lost the attack on {attackedteam.teamname} and lost {lostpoints} FP" )
        newnotif.save()
        notifattacked = Notif(user=room.user, room=room, context=f'Somebody attacked and you won!  {lostpoints} flagpoints were awarded to you. ')
        notifattacked.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            room.roomname,
            {
                'type': 'chat_message',
                'status': 'win',
                'message': f'Somebody attacked and you won!  {lostpoints} flagpoints were awarded to you. '
            }
        )
    return HttpResponse(status)

@require_http_methods(["POST"])
def poison(request):
    if not request.session.get('name'):
        return redirect('dashboard:login')
    if 'team' in request.session.get('team'):
        return redirect('dashboard:dashboard')
    name= request.session.get('name')[0]
    q = User.objects.get(p1name=name)
    teamname = request.POST.get('teamname')
    powerup = PowerUp.objects.get(user=q)
    if not User.objects.filter(p1name=teamname).exists():
        hacweb.send(f"{q.teamname} tried to poison null team.")
        return HttpResponse("hack")
    team =  User.objects.get(p1name=teamname)
    if powerup.poison == 0:
        hacweb.send(f"{q.teamname} tried to poison with no poison powerup")
        return HttpResponse("reload")
    hfp = HourlyFp.objects.get(user=team)
    if hfp.poisoned:
        return HttpResponse('reload')
    hfp.poisoned = True
    hfp.poisonedtill = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=3)
    hfp.save()
    powerup.poison -= 1
    powerup.save()
    request.session['poison'] = team.teamname
    channel_layer = get_channel_layer()
    room = Room.objects.get(user=team)
    room2 = Room.objects.get(user=q)
    newnotif = Notif(user=room2.user, room=room2, context=f"You used your poison on {team.teamname}" )
    newnotif.save()
    notifattacked = Notif(user=room.user, room=room, context=f'Somebody has poisoned you! Your hourly flag points are now stopped for 3 hours. ')
    notifattacked.save()
    async_to_sync(channel_layer.group_send)(
        room.roomname,
        {
            'type': 'chat_message',
            'status': 'lose',
            'message': f'Somebody has poisoned you! Your hourly flag points are now stopped for 3 hours. '
        }
    )
    if team.p2discord:
        p2discord = team.p2discord
    else:
        p2discord = "NA"
    if team.p3discord:
        p3discord = team.p3discord
    else:
        p3discord = "NA"
    notifyweb.send(f"{team.p1discord}, {p2discord}, {p3discord}, Master! You were poisoned and your hourly flag points are now stopped for 3 hours.")
    return HttpResponse('poisoned')
def questions(request):
    if not request.session.get('name'):
        return redirect('dashboard:login')
    if 'team' in request.session.get('team'):
        return redirect('dashboard:dashboard')
    ques = Question.objects.all()

    quest = []
    name= request.session.get('name')[0]
    q = User.objects.get(p1name=name)
    if name != "Admin":
        return redirect('dashboard:dashboard')
    for qu in ques:
        check = CheckQues.objects.get(team=q, question=qu)
        quest.append({"ques": qu.heading, "solved": check.solved})

    if not CurrentQues.objects.filter(team=q).exists():
        f = CurrentQues(team=q)
        f.save()

    else:
        f = CurrentQues.objects.get(team=q)
        if f.question:
            current = f.question
            return redirect("questions:quest")
    room = Room.objects.get(user=q)
    if request.session.get('correct'):
        timetaken = request.session.get('correct')['time']
        bp = request.session.get('correct')['bp']
        request.session.pop('correct')
        return render(request,"questions.html", {"questions": quest, "time": timetaken, "bp": bp, "room": room.roomname})

    return render(request,"questions.html", {"questions": quest, "room": room.roomname})

def wow(request):
    return redirect("https://open.spotify.com/track/4dgeKnbKybBMEHlNTkoCpX")
def logout(request):
    request.session.flush()
    return redirect("dashboard:login")
