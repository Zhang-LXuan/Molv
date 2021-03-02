from django.db import models

# Create your models here.
import datetime
from django.utils import timezone
# Create your models here.
class Question(models.Model):
    question_text=models.CharField(max_length=200)
    pub_date=models.DateTimeField('date published')
    matched_nums=models.IntegerField(default=0)
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    
class Answer(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    answer_text=models.CharField(max_length=10000)
    video_url=models.CharField(max_length=50,default='')
    image_url=models.CharField(max_length=50,default='')
    def __str__(self):
        return self.answer_text
    def __str__(self):
        return self.video_url
    def __str__(self):
        return self.image_url


