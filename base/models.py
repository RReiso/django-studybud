from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    # 1 to many : 1 host can have many rooms
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # 1 to many : 1 topic can have many rooms
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)

    # value and form(that user can fill in) can be blank
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)  # everytime on save

    # only when first create instance
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']  # reverse order

    def __str__(self):
        return self.name


class Message(models.Model):
    # 1 to many : 1 user can have many messages
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # 1 to many : 1 room can have many messages
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()  # message body
    updated = models.DateTimeField(auto_now=True)  # everytime on save
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']  # reverse order

    def __str__(self):
        return self.body[0:50]  # first 50 characters
