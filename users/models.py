from django.db import models
import datetime
import string
import random


N = 7




class User(models.Model):
    teamname = models.CharField(max_length=200)
    p1name = models.CharField(max_length=200)
    p1email = models.CharField(max_length=200)
    p2name = models.CharField(max_length=200)
    p2email = models.CharField(max_length=200)
    p3name = models.CharField(max_length=200)
    p3email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    def __str__(self):
        return self.teamname
    def save(self, force_insert=False, force_update=False):
        is_new = self.id is None
        super(User, self).save(force_insert, force_update)
        if is_new:
            res = ''.join(random.choices(string.ascii_uppercase +
                                         string.digits, k = N))
            Points.objects.create(user=self)
            Troops.objects.create(user=self)
            Cooldown.objects.create(user=self)
            PowerUp.objects.create(user=self)
            HourlyFp.objects.create(user=self)
            Room.objects.create(user=self, roomname=res)

class Points(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    flagpoints = models.IntegerField(default=0)
    battlepoints = models.IntegerField(default=0)
    defensepoints = models.IntegerField(default=0)
    attackpoints = models.IntegerField(default=0)
    recentupdate =  models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.user.teamname
class Troops(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    soldiers = models.IntegerField(default=0)
    tanks = models.IntegerField(default=0)
    bombers = models.IntegerField(default=0)
    aag = models.IntegerField(default=0)
    def __str__(self):
        return self.user.teamname

class Cooldown(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shield = models.DateTimeField(blank=True, null=True)
    attack = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.user.teamname

class PowerUp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    multiplier = models.IntegerField(default=0)
    poison = models.IntegerField(default=0)
    hp = models.IntegerField(default=0)
    bonusfp = models.IntegerField(default=0)
    def __str__(self):
        return self.user.teamname

class HourlyFp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recent = models.DateTimeField(blank=True, null=True)
    poisoned = models.BooleanField(default=False)
    poisonedtill = models.DateTimeField(blank=True, null=True)
    bonusfp = models.BooleanField(default=False)
    bonustill = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.user.teamname

class Room(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roomname = models.CharField(max_length=200)

class Notif(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    context = models.TextField()
