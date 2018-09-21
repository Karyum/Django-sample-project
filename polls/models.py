import datetime

from django.db import models
from django.utils import timezone
# Create your models here.
class Question(models.Model):
    '''
        Question model holds text for the question
        and the date it was published
    '''
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    '''
     Choice model holds the key relating to the question and a string
     of what is the choice_text and how many votes
    '''
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
