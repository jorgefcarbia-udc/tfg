from django.urls import path

from . import views

app_name = "chat"
urlpatterns = [
    path("login", views.login_user, name="login"),
    path("signup", views.signup, name="signup"),
    path("logout_user", views.logout_user, name="logout_user"),
    path("user/<int:user_id>/home", views.home, name="home"),
    path("user/<int:user_id>/chats", views.chats, name="chats"),
    path("<int:chat_id>/message", views.message, name="message"),
    path("<int:chat_id>", views.chat, name="chat"),
    path("<int:chat_id>/delete", views.delete_chat, name="delete_chat"),
    path("dataload", views.dataload, name="dataload"),
    path("<int:chat_id>/download/<str:file_name>", views.download_file, name="download"),
]