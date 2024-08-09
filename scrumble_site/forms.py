from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

def change_style(self, css_class, widgets = None):
    if widgets is None:
        widgets = self.visible_fields()
    for widget in widgets:
        widget.field.widget.attrs['class'] = css_class
        widget.field.widget.attrs['placeholder'] = widget.field.label

class LoginForm(forms.Form):
    username = forms.CharField(max_length=128, label="Логин", required=True)
    password = forms.CharField(max_length=128, label="Пароль", widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        change_style(self, 'input input-sm w-full max-w-xs mt-3 rounded-md')

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1','password2'] 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        change_style(self, 'input input-sm w-full max-w-xs mt-3 rounded-md')
