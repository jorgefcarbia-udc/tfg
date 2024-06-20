from django.contrib import admin
from .models import UDCUser, Chat, Message, UserType

admin.site.register(UDCUser)
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(UserType)
