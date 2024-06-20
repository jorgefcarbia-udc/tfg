import os 
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages.test import MessagesTestMixin
from django.contrib import messages

from chat.models import UDCUser, UserType, Chat, Message
from chat.core.core_service import CoreService 
from chat.settings import FILE_DATA_ROOT_FOLDER

class LoginUserViewTest(TestCase, MessagesTestMixin):
    def setUp(self):
        self.auth_user = User.objects.create_user('alan.smithee', 'alan.smithee@udc.es', 'Aa123456')
        self.udc_user = UDCUser.objects.create(user=self.auth_user, login_name='alan.smithee', full_name='Alan Smithee', user_type=UserType.objects.create(type="Student"))

    def test_login_user_get(self):
        response = self.client.get(reverse('chat:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/login.html')

    def test_login_user_post_success(self):
        response = self.client.post(reverse('chat:login'), {'username': 'alan.smithee', 'password': 'Aa123456'})
        self.assertRedirects(response, reverse('chat:home', args=(self.udc_user.id,))) 

    def test_login_user_post_fail(self):
        response = self.client.post(reverse('chat:login'), {'username': 'john'})
        self.assertTrue('form' in response.context) 
        form = response.context['form']
        self.assertTrue(form.is_bound) 
        self.assertFalse(form.is_valid()) 

class LogoutUserViewTest(TestCase):
    def test_logout_user(self):
        response = self.client.get(reverse('chat:logout_user'))
        self.assertRedirects(response, reverse('chat:login'))

class SignupViewTest(TestCase):
    def setUp(self):
        self.user_type = UserType.objects.create(type="Student")

    def test_signup_user_get(self):
        response = self.client.get(reverse('chat:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/signup.html')

    def test_signup_user_post_success(self):
        response = self.client.post(reverse('chat:signup'), {
            'username': 'newuser', 
            'password1': 'testpassword123', 
            'password2': 'testpassword123',
            'email': 'newuser@example.com',
            'full_name': 'New User',
            'user_type': self.user_type.id
        })
        self.assertEqual(UDCUser.objects.count(), 1)
        self.assertRedirects(response, reverse('chat:home', args=(UDCUser.objects.first().id,)))

    def test_signup_user_post_fail(self):
        response = self.client.post(reverse('chat:signup'), {
            'username': 'newuser', 
            'password1': 'testpassword',
            'password2': 'testpassword'
            })
        self.assertTrue('form' in response.context)
        self.assertFalse(response.context['form'].is_valid())


class HomeViewTest(TestCase):
    def setUp(self):
        self.user_type = UserType.objects.create(type="Admin")
        self.user = User.objects.create_user('john', 'john@example.com', 'johnpassword')
        self.udc_user = UDCUser.objects.create(user=self.user, login_name=self.user.username, full_name="John Doe", user_type=self.user_type)

    def test_home_user_get(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('chat:home', args=(self.udc_user.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/home.html')

    def test_home_user_post_message(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.post(reverse('chat:home', args=(self.udc_user.id,)), {'chat_message': 'Hello!'})
        last_chat_id = self.udc_user.get_last_chats(1)[0].id
        self.assertRedirects(response, reverse('chat:chat', args=(last_chat_id,)))

class DataLoadViewTest(TestCase):
    def setUp(self):
        response = self.client.post(reverse('chat:dataload'))
        self.assertRedirects(response, reverse('chat:login'))

class ChatListViewTest(TestCase):
    def setUp(self):
        self.user_type = UserType.objects.create(type="Admin")
        self.user = User.objects.create_user('john', 'john@example.com', 'johnpassword')
        self.udc_user = UDCUser.objects.create(user=self.user, login_name=self.user.username, full_name="John Doe", user_type=self.user_type)
        Chat.objects.bulk_create([Chat(user=self.udc_user) for i in range(5)])

    def test_chat_list_view(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('chat:chats', args=(self.udc_user.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['chats']), 5)

class DeleteChatViewTest(TestCase):
    def setUp(self):
        self.user_type = UserType.objects.create(type="Admin")
        self.user = User.objects.create_user('john', 'john@example.com', 'johnpassword')
        self.udc_user = UDCUser.objects.create(user=self.user, login_name=self.user.username, full_name="John Doe", user_type=self.user_type)
        Chat.objects.bulk_create([Chat(user=self.udc_user) for i in range(5)])

    def test_delete_chat_view(self):
        self.client.login(username='john', password='johnpassword')
        self.assertEqual(Chat.objects.count(), 5)
        chat_id = self.udc_user.get_last_chats(1)[0].id
        response = self.client.get(reverse('chat:delete_chat', args=(chat_id,)))
        self.assertRedirects(response, reverse('chat:chats', args=(self.udc_user.id,)))
        self.assertEqual(Chat.objects.count(), 4)

    def test_send_message_chat_view(self):
        self.client.login(username='john', password='johnpassword')
        last_chat= self.udc_user.get_last_chats(1)[0]
        response = self.client.post(reverse('chat:message', args=(last_chat.id,)), {'chat_message': 'Hello!'})
        self.assertRedirects(response, reverse('chat:chat', args=(last_chat.id,)))
        self.assertEqual(len(last_chat.get_ordered_messages()), 2)
        self.assertEqual(last_chat.get_ordered_messages()[0].content, 'Hello!')


class DownloadFileViewTest(TestCase):
    def setUp(self):
        self.user_type = UserType.objects.create(type="Admin")
        self.user = User.objects.create_user('john', 'john@example.com', 'johnpassword')
        self.udc_user = UDCUser.objects.create(user=self.user, login_name=self.user.username, full_name="John Doe", user_type=self.user_type)

        self.folder_path = FILE_DATA_ROOT_FOLDER + "/test_get_data_to_load"
        os.makedirs(self.folder_path, exist_ok=True)
        text = "This is a test\n\n\n\n"
        self.file_name = "test.txt"
        self.file_path = self.folder_path + "/" + self.file_name
        with open(self.file_path, 'w') as file:
            file.write(text)

    def test_download_file_view(self):
        self.client.login(username='john', password='johnpassword')
        chat = Chat.objects.create(user=self.udc_user)
        context = chat.context_set.create(source="Filesystem", location=self.file_path, title=self.file_name)
        response = self.client.get(reverse('chat:download', args=(chat.id, 'test.txt')))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="test.txt"')

        os.remove(self.file_path)
        os.removedirs(self.folder_path)