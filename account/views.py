from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm,\
                    UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib import messages

def user_login(request):
    '''Instantiate the form with the submitted data with form =
LoginForm(request.POST).'''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        '''Check whether the form is valid with form.is_valid(). If it is not
valid, we display the form errors in our template'''
        if form.is_valid():
            cd = form.cleaned_data
            '''If the user is not active, we
return an HttpResponse that displays the Disabled'''
            user = authenticate(request,
                        username=cd['username'],
                        password=cd['password'])

            if user is not None: #we check whether the user is active, accessing its is_active attribute.
                if user.is_active:
                    '''If the user is active, we log the user into the website.'''
                    login(request, user)
                    return HttpResponse('Authenticated' \
                                        'Successfully')

                else:
                    '''If the user is not active, we
return an HttpResponse that displays the Disabled'''
                    return HttpResponse('Disabled account')

            else:
                return HttpResponse('Invalid Login')

    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

    '''Note the difference between authenticate and login: authenticate() checks user
credentials and returns a User object if they are right; login() sets the user in
the current session.'''


############################################################
'''create a new view to display a dashboard when users
log in to their account'''

'''If the user is authenticated, it executes the decorated view; if the user is not authenticated, it redirects the user to the login URL'''
'''we added a hidden input in the form of our login template for this purpose.'''
@login_required  #The login_required decorator checks whether the current user is authenticated
def dashboard(request):
    return render(request,
                    'accounts/dashboard.html',
                    {'section': 'dashboard'})
'''We also define a section variable. We will use this variable to track
the site's section that the user is browsing.'''

#############################################################
#############registration view###############################

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
           # Create a new user object but avoid saving it yet
           new_user = user_form.save(commit=False)
           # Set the chosen password
           '''set_password() method of the user model that handles encryption to save for safety
reasons.'''
           new_user.set_password(
               user_form.cleaned_data['password']
           )
           # Save the User object
           new_user.save()
           # create the user profile
           Profile.objects.create(user=new_user)
           '''When users register on our site, we will create an empty profile
associated with them. You should create a Profile object manually
using the administration site for the users you created before.'''
           return render(request,
                        'accounts/register_done.html',
                        {'new_user': new_user})

    else:
        user_form = UserRegistrationForm()
    return render(request,
                'accounts/register.html',
                {'user_form': user_form})

# We use the login_required decorator because users have to be
# authenticated to edit their profile
@login_required
def edit(request):
    '''
    we use 2 model forms:
    userEditform:store the data of the built-in user model,
    ProfileEditForm:store the additional profile data in the
custom Profile model.
    '''
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                        data=request.POST)
        profile_form = ProfileEditForm(
                        instance=request.user.profile,
                        data=request.POST,
                        files=request.FILES)
# To validate the submitted data, we will execute the is_valid() method of both forms
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save() #save the form
            profile_form.save()
            # using the message framewor
            messages.success(request, 'Profile update'\
                                    'successfuly')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
                        instance=request.user.profile)

    return render(request, 
                    'accounts/edit.html',
                    {'user_form': user_form,
                    'profile_form': profile_form})


