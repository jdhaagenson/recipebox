from cookbook.models import Author
from django import forms
from django.contrib.auth.forms import UserCreationForm


class AddRecipeForm(forms.Form):
    title = forms.CharField(max_length=50)
    author = forms.ModelChoiceField(Author.objects.all())
    description = forms.CharField(widget=forms.Textarea)
    time_required = forms.CharField(max_length=50)
    instructions = forms.CharField(widget=forms.Textarea)


class AddAuthorForm(forms.ModelForm):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Author
        fields = [
            'name',
            'bio'
        ]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)


# class SignupForm(UserCreationForm):
#     username = forms.CharField(max_length=240)
#     password = forms.CharField(widget=forms.PasswordInput)
#     class Meta:
#         model = Author
#         fields = ('username', 'password', 'name', 'bio')

