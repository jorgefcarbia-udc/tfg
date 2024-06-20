from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserType
from . import settings

class UserTypeChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.type

class SignupForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True)
    user_type = UserTypeChoiceField(queryset=UserType.get_active_user_types(), required=True, initial=1)
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2', 'email',]

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = "Nome de usuario"
        self.fields['password'].widget.attrs['placeholder'] = "Contrasinal"

class ChatForm(forms.Form):
    chat_message = forms.CharField(max_length=settings.MAX_QUESTION_LENGTH)

class HomeForm(forms.Form):
    chat_message = forms.CharField(max_length=settings.MAX_QUESTION_LENGTH)

    def __init__(self, *args, **kwargs):
        super(HomeForm, self).__init__(*args, **kwargs)
        self.fields['chat_message'].widget.attrs['placeholder'] = "En que che podo axudar?"
        self.fields['chat_message'].widget.attrs['name'] = "chat_message"

