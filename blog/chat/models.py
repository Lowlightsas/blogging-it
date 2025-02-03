from django.db import models
from django.contrib.auth.models import User
class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128,unique=True)
    

    def __str__(self):
        return self.group_name
    
class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE,related_name='chat_messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author.username} : {self.group.group_name}'
    
    class Meta:
        ordering = ['-created']