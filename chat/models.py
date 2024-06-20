from typing import *
from django.db import models
from django.contrib.auth.models import User
from dataclasses import dataclass
from django.db.models import QuerySet


class UserType(models.Model):
    type = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    def __str__(self):
        return f"UserType(type={self.type}, active={self.active})"
    def get_active_user_types():
        return UserType.objects.filter(active=True)

class UDCUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    login_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100)
    creation_time = models.DateTimeField(auto_now_add=True)
    last_login_time = models.DateTimeField(blank=True, null=True)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    def get_chats(self):
        return self.chat_set.all().order_by("-creation_time")
    def get_last_chats(self, chat_limit):
        return self.chat_set.all().order_by("-creation_time")[:chat_limit]
    def is_admin(self):
        return self.user_type.type == "Admin"
    def __str__(self):
        return f"UDCUser(user= {self.user}, login_name={self.login_name}, full_name={self.full_name},creation_time={self.creation_time},last_login_time={self.last_login_time},user_type={self.user_type},active={self.active})"

class Message(models.Model):
    class MessageOrigin(models.TextChoices):
        USER = "U"
        GPT = "G"
    origin = models.CharField(
        max_length = 1,
        choices = MessageOrigin,
    )
    content = models.TextField(default="")
    creation_time = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey("Chat", on_delete=models.CASCADE)
    def __str__(self):
        return f"Message(creation_time={self.creation_time},origin={self.origin},chat={self.chat},content={self.content})"

class Context(models.Model):
    chat = models.ForeignKey("Chat", on_delete=models.CASCADE)
    source = models.TextField(default="")
    location = models.TextField(default="")
    title = models.TextField(default="")
    relevance = models.FloatField(default=0)
    def is_file(self):
        return self.source == "Filesystem"
    def __str__(self):
        return f"Context(chat={self.chat},source={self.source},location={self.location},title={self.title},relevance={self.relevance})"
 

class Chat(models.Model):
    class ChatStatus(models.TextChoices):
        ACTIVE = "ACT", "Active"
        EXPIRED = "EXP", "Expired"
    status: models.CharField = models.CharField(
        max_length=3,
        choices=ChatStatus.choices,
        default=ChatStatus.ACTIVE,
    )
    creation_time:  models.DateTimeField = models.DateTimeField(auto_now_add=True)
    last_update_time: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    user: models.ForeignKey[UDCUser] = models.ForeignKey(UDCUser, on_delete=models.CASCADE)
   
    def get_last_messages(self, message_limit: int) -> QuerySet[Message]:
        return self.message_set.all().order_by("-creation_time")[:message_limit]
    def get_user_first_message(self) -> Optional[Message]:
        return self.message_set.filter(origin=Message.MessageOrigin.USER).first()
    def get_ordered_messages(self) -> QuerySet[Message]:
        return self.message_set.all().order_by("creation_time")
    def get_all_context(self) -> QuerySet[Context]:
        return self.context_set.all()
    def get_top_context(self) -> QuerySet[Context]:
        return self.context_set.all().order_by("-relevance")[:3]
    def get_file_context(self, file_name: str) -> Optional[Context]:
        return self.context_set.filter(source="Filesystem", title=file_name).first()
    def __str__(self):
        return f"Chat(status={self.status},creation_time={self.creation_time},last_update_time={self.last_update_time},user={self.user})"


