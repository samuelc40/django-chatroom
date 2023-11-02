from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50, blank=False, null=True)
    last_name = models.CharField(max_length=50, blank=False, null=True)
    profile_picture = models.ImageField(upload_to='img', blank=False, null=True, default='default-profile.jpg')
    friends = models.ManyToManyField(User, blank=True, related_name='friend_profiles')

    def __str__(self):
        return self.username

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} sent {self.receiver.username} a friend request"
    
class Notification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender_notification")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver_notification")
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    seen = models.BooleanField(default=False)


    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"Hi {self.sender.username} accepted Your friend request"
    
class Friend(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='friend_relation') # Change related_name

    def __str__(self):
        return self.profile.username
    
class ChatMessage(models.Model):
    body = models.TextField()
    msg_sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="msg_sender")
    msg_receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="msg_receiver")
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.body


