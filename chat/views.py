from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, FileResponse
from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from .models import UDCUser, Chat, Message, Context, UserType
from .forms import LoginForm, SignupForm, ChatForm, HomeForm
from .core.core_service import *

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                udc_user_obj = get_object_or_404(UDCUser, user=user)
                return HttpResponseRedirect(reverse("chat:home", args=(udc_user_obj.id,)))
    else:
        form = LoginForm()
    return render(request, 'chat/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('chat:login'))


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            user_type = form.cleaned_data['user_type']
            internal_user = form.save()
            try:
                udc_user = UDCUser(user=internal_user, login_name=internal_user.username, full_name=full_name, user_type=user_type)
                udc_user.save()
            except Exception as e:
                internal_user.delete()
            return HttpResponseRedirect(reverse("chat:home", args=(udc_user.id,)))
        else:
           print(form.errors.as_data())
    else:
        form = SignupForm()
    return render(request, 'chat/signup.html', {'form': form})


def home(request, user_id):
    user_obj = get_object_or_404(UDCUser, pk=user_id)
    if request.method == "POST":
        form = HomeForm(request.POST)
        if form.is_valid():
            new_chat = Chat(user=user_obj)
            new_chat.save()

            user_message_text = form.cleaned_data["chat_message"]
            user_message = Message(content = user_message_text, origin = Message.MessageOrigin.USER, chat = new_chat)
            
            gpt_response_text, context = CoreService.get_LLM_response(user_message_text, [])
            gpt_message = Message(content = gpt_response_text, origin = Message.MessageOrigin.GPT, chat = new_chat)

            Message.objects.bulk_create([user_message, gpt_message])
            Context.objects.bulk_create([Context(chat=new_chat, source=data.get_metadata()["source"], location=data.get_metadata()["location"], title=data.get_metadata()["title"]) for data in context])
            
            return HttpResponseRedirect(reverse("chat:chat", args=(new_chat.id,)))
    else:
        form = HomeForm()
        user_chats = []
        for user_chat in user_obj.get_last_chats(3):
            user_data = {"chat": user_chat, "first_user_message": user_chat.get_user_first_message()}
            user_chats.append(user_data)
        return render(request, "chat/home.html", {"user": user_obj, "chats": user_chats, "form": form})


def chats(
        request: HttpRequest, 
        user_id: int) -> HttpResponse:
    user_obj: UDCUser = get_object_or_404(UDCUser, pk=user_id)
    user_chats: List[Chat] = user_obj.get_chats()
    
    return render(request, "chat/chats.html", {"user": user_obj, "chats": user_chats})


def chat(request, chat_id):
    chat_obj = get_object_or_404(Chat, pk=chat_id)
    if request.method == "POST":
        return HttpResponseRedirect(reverse("chat:chat", args=(chat_obj.id,)))
    else:
        return render(request, "chat/chat.html", {"chat": chat_obj})

def delete_chat(request, chat_id):
    chat_obj = get_object_or_404(Chat, pk=chat_id)
    user_obj = chat_obj.user
    chat_obj.delete()
    return HttpResponseRedirect(reverse("chat:chats", args=(user_obj.id,)))

def message(request, chat_id):
    chat_obj = get_object_or_404(Chat, pk=chat_id)
    user_message_text = request.POST["chat_message"]
    user_message = Message(content = user_message_text, origin = Message.MessageOrigin.USER, chat = chat_obj)
    last_messages_data = [MessageData(message.content, message.origin) for message in chat_obj.get_last_messages(5)]
    gpt_response_text, context = CoreService.get_LLM_response(user_message_text, last_messages_data)
    gpt_message = Message(content = gpt_response_text, origin = Message.MessageOrigin.GPT, chat = chat_obj)
    Message.objects.bulk_create([user_message, gpt_message])
    return HttpResponseRedirect(reverse("chat:chat", args=(chat_obj.id,)))


def dataload(request):
    CoreService.load_vector_storage()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse("chat:login")))

def download_file(request, chat_id, file_name):
    chat_obj = get_object_or_404(Chat, pk=chat_id)
    context_obj = chat_obj.get_file_context(file_name)
    filepath = context_obj.location
    filename = context_obj.title
    return FileResponse(open(filepath, 'rb'), as_attachment=True, filename=filename)