from django import forms
from django.contrib.auth.models import User
from .models import Profile

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
# we will add forms to let users edit their profile on the website
'''UserEditForm: This will allow users to edit their first name, last
name, and email, which are attributes of the built-in Django
user model.'''
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

'''ProfileEditForm: This will allow users to edit the profile data we
save in the custom Profile model. Users will be able to edit
their date of birth and upload a picture for their profile'''
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('data_of_birth', 'photo')