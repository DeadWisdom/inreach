from django.forms import ModelForm, PasswordInput

from models import Account

class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['address', 'port', 'login', 'password', 'search', 'send_to_twitter']
        #widgets = { 'password': PasswordInput() }