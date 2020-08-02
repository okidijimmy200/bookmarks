from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    '''PasswordInput widget to render its HTML input
element, including a type="password" attribute, so that the browser
treats it as a password input.'''
    password = forms.CharField(widget=forms.PasswordInput)