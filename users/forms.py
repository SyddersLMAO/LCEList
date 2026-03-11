from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from .models import User

input_classes = "w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-sm text-gray-100 focus:outline-none focus:border-pink-300"

class StyledLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = input_classes

    def clean(self):
        username = self.cleaned_data.get('username')
        if username:
            try:
                user = User.objects.get(username__iexact=username)
                self.cleaned_data['username'] = user.username
            except User.DoesNotExist:
                pass
        return super().clean()

class StyledRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = input_classes