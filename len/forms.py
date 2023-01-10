from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm, TextInput, CheckboxInput, Select, NumberInput, EmailInput, PasswordInput, DateInput
from .models import Clients, Contacts, ClientsContacts
from django import forms
from django.contrib.auth.models import User


class ClientForm(ModelForm):
    class Meta:
        model = Clients
        fields = ('name', 'fcs', 'client_type', 'client_status')

        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Псевдоним",
                'required': True,
            }),

            "fcs": TextInput(attrs={
                'class': 'form-control',
                'placeholder': "ФИО",
                'required': True,
            }),

            "client_status": Select(attrs={
                'class': 'form-control',
                'required': True,
            }),

            "client_type": Select(attrs={
                'class': 'form-control',
                'required': True,
            }),
        }


class ClientsContactsForm(ModelForm):
    class Meta:
        model = ClientsContacts
        fields = ('contacts_type',)

        widgets = {
            "contacts_type": Select(attrs={
                'class': 'form-control',
                'required': True,
            }),
        }


class ContactForm(ModelForm):
    class Meta:
        model = Contacts
        fields = ('first_name', 'last_name', 'middle_name', 'phone', 'birthday', 'ban_on_spam')

        widgets = {
            "first_name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Имя",
                'required': True,
            }),
            "last_name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Фамилия",
                'required': True,
            }),
            "middle_name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Отчество",
                'required': True,
            }),
            "phone": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Номер телефона",
                'required': True,
            }),
            "birthday": DateInput(attrs={
                'blank': True,
                'class': 'form-control',
                'type': 'date'
            }),
            "ban_on_spam": CheckboxInput(attrs={
                'class': 'form-check-input',
            })
        }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': "Логин"
    }))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-input',
        'placeholder': "Пароль"
    }))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={
        'class': 'form-input',
        'placeholder': "Повтор пароля"
    }))
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={
        'class': 'form-input',
        'placeholder': "E-mail",
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': "Логин"
    }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-input',
        'placeholder': "Пароль"
    }))
