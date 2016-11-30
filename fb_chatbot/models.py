from django.db import models

# Create your models here.

class UserDetail(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)

class MessageDB(models.Model):
    message_text = models.CharField(max_length=300)
    user_id = models.CharField(max_length=50)    
