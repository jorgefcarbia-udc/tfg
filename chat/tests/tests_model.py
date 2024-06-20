from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from chat.models import UserType, UDCUser, Message, Chat, Context

class UDCUserTestCase(TestCase):
    def setUp(self):
        user_type = UserType.objects.create(type="UserTest", active=True)
        auth_user = User.objects.create(username='john')
        self.udc_user = UDCUser.objects.create(user=auth_user, login_name='john123', full_name='John Doe', user_type=user_type, active=True)

    def test_get_chats(self):
        self.assertEqual(len(self.udc_user.get_chats()), 0)

        chat = Chat.objects.create(user=self.udc_user)
        self.assertEqual(len(self.udc_user.get_chats()), 1)
        self.assertEqual(self.udc_user.get_chats()[0], chat)
        self.assertEqual(self.udc_user.get_chats()[0].user, self.udc_user)

    def test_get_last_chats(self):
        self.assertEqual(len(self.udc_user.get_last_chats(2)), 0)

        chat1 = Chat.objects.create(user=self.udc_user)
        chat2 = Chat.objects.create(user=self.udc_user)
        chat3 = Chat.objects.create(user=self.udc_user)
        chat4 = Chat.objects.create(user=self.udc_user)
        chat5 = Chat.objects.create(user=self.udc_user)

        self.assertEqual(len(self.udc_user.get_last_chats(3)), 3)
        self.assertEqual(len(self.udc_user.get_last_chats(5)), 5)
        self.assertEqual(len(self.udc_user.get_last_chats(10)), 5)
        self.assertEqual(self.udc_user.get_last_chats(3)[0], chat5)
        self.assertEqual(self.udc_user.get_last_chats(3)[1], chat4)
        self.assertEqual(self.udc_user.get_last_chats(3)[2], chat3)
        self.assertEqual(self.udc_user.get_last_chats(3)[0].user, self.udc_user)

class MessageTestCase(TestCase):
    def setUp(self):
        self.chat = Chat.objects.create()  # Add necessary parameters
        self.message = Message.objects.create(chat=self.chat, origin=Message.MessageOrigin.USER, content="Hello, World!")  

class ChatTestCase(TestCase):
    def setUp(self):
        self.user_type = UserType.objects.create(type="UserTest", active=True)
        self.auth_user = User.objects.create(username='john')
        self.user = UDCUser.objects.create(user=self.auth_user, user_type=self.user_type, login_name="testuser", full_name="Test User")  # Add necessary parameters
        self.chat = Chat.objects.create(user=self.user)
        messages = [Message.objects.create(chat=self.chat, origin=Message.MessageOrigin.USER, content="Message number " + str(i)) for i in range(10)]
        context = [Context.objects.create(chat=self.chat, source="File", location="/dev/null", title="Context number " + str(i), relevance=0.1*i) for i in range(10)]

    def test_get_last_messages(self):
        messages = self.chat.get_last_messages(2)
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0].content, "Message number 9")
        self.assertEqual(messages[1].content, "Message number 8")
    
    def test_get_user_first_message(self):
        self.assertEqual(self.chat.get_user_first_message().content, "Message number 0")
        self.assertEqual(self.chat.get_user_first_message().origin, Message.MessageOrigin.USER)

    def test_get_ordered_messages(self):
        messages = self.chat.get_ordered_messages()
        self.assertEqual(len(messages), 10)
        for i in range(10):
            self.assertEqual(messages[i].content, "Message number " + str(i))
    
    def test_get_all_context(self):
        context = self.chat.get_all_context()
        self.assertEqual(len(context), 10)
        self.assertEqual(context[0].title, "Context number 0")
        self.assertEqual(context[7].title, "Context number 7")

    def test_get_top_context(self):
        context = self.chat.get_top_context()
        self.assertEqual(len(context), 3)
        self.assertEqual(context[0].title, "Context number 9")
        self.assertEqual(context[1].title, "Context number 8")
        self.assertEqual(context[2].title, "Context number 7")
