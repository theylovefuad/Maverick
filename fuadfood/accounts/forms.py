from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserCreationForm(UserCreationForm):
    mobile = forms.IntegerField(required=True, )
    state = forms.CharField()
    first_name = forms.CharField( required=False, help_text='Optional')
    last_name = forms.CharField( required=False, help_text='Optional')
    email = forms.EmailField( help_text='Enter a valid email address')
    class Meta:
        model= User
        fields=[
            'username',
            'first_name',
            'last_name',
            'email',
            'state',
            'mobile',
            'password1',
            'password2',
        ]
        labels = {'mob':'Mobile Number', 'state': 'State of Residence',}
   