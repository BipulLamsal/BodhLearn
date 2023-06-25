from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name 

class Point(models.Model):
    user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    points = models.IntegerField()
    def __str__(self):
        return self.user.username 

class Profile(models.Model):
    user = models.OneToOneField(User,related_name='extendprofile',on_delete=models.CASCADE)
    following = models.ManyToManyField(User,related_name='following',blank=True)
    follower = models.ManyToManyField(User,related_name='follower',blank=True)
    profile_img = models.ImageField(default='imgs/profiles_img/default_pic.jpg', upload_to = 'imgs/profiles_img', null=True, blank=True)
    cover_img = models.ImageField(default='imgs/cover_img/default.jpg', upload_to = 'imgs/cover_img', null=True, blank=True)

class Question(models.Model):
    host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    like = models.ManyToManyField(User,related_name='like_post',blank=True)
    dislike = models.ManyToManyField(User,related_name='dislike_post',blank=True)
    point = models.IntegerField(null=True,blank=True,default=0)
    participants = models.ManyToManyField(User,related_name='participants',blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated','-created']
    
    
    def __str__(self):
        return self.name  

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    message = models.TextField()
    like = models.ManyToManyField(User,related_name='like_message',blank=True)
    dislike = models.ManyToManyField(User,related_name='dislike_message',blank=True)
    # correct = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']
        
    def __str__(self):
        return self.message[0:50]

class CorrectAnswer(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    message = models.ForeignKey(Message,on_delete=models.CASCADE)
    def __str__(self):
        return self.message.message  

