from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    '''PasswordInput widget to render its HTML input
element, including a type="password" attribute, so that the browser
treats it as a password input.'''
    password = forms.CharField(widget=forms.PasswordInput)

'''we include only the username, first_name, and email fields of the model. These
fields will be validated based on their corresponding model fields'''

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    '''define a clean_password2() method to check the second password against the
first one and not let the form validate if the passwords don't match'''
    def clean_password2(self):
        '''clean_password2()  check is done when we validate the form calling its is_valid()
method.'''
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')

        return cd['password2']
