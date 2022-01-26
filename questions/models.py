from django.db import models
from users.models import User
import datetime
# Create your models here.
class Question(models.Model):
    heading = models.CharField(max_length=250, default="f")
    context = models.TextField()
    answer = models.TextField()
    def save(self, force_insert=False, force_update=False):
        is_new = self.id is None
        super(Question, self).save(force_insert, force_update)
        if is_new:
            for u in User.objects.all():
                CheckQues.objects.create(team=u, question=self)
                

class CheckQues(models.Model):
    team = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    solved = models.BooleanField(default=False)
    starttime = models.DateTimeField(null=True, blank=True)
    endtime = models.DateTimeField(null=True, blank=True)

class CurrentQues(models.Model):
    team = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
