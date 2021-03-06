from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm,\
                    UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from .models import Contact
from actions.utils import create_action
from actions.models import Action

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
    # Display all actions by default   
# retrieve all actions from the database, excluding the ones performed by the current user.
    actions = Action.objects.exclude(user=request.user)
# By default, you retrieve the latest actions performed by all users on the platform.
# ----------------------------------------------------------------------------
# If the user is following other users, you restrict the query to retrieve only the actions performed by the users they follow.
    following_ids = request.user.following.values_list('id',
                                                       flat=True)

    if following_ids:
    # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
# Finally, you limit the result to the first 10 actions returned.
    actions = actions.select_related('user', 'user__profile')\
                     .prefetch_related('target')[:10] #user__profile to join the Profile table in a single SQL query and if no arguments is passed to it, it will retrieve objects from all ForeignKey relationships.
# This query is now optimized for retrieving the user actions, including related objects. 

# SELECT RELATED: allows you to retrieve related objects for one-to-many relationships wch is for is for ForeignKey and OneToOne fields.
    return render(request,
                    'accounts/dashboard.html',
                    {'section': 'dashboard',
                    'actions': actions})
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
           create_action(new_user, 'has created an account')
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
# we use 2 model forms: userEditform:store the data of the built-in user model,
# ProfileEditForm:store the additional profile data in the custom Profile model
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
            # using the message framework
            messages.success(request, 'Profile update successfuly')
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

@login_required
# The user_list view gets all active users.
# NB: you cld add pagination to the users available
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,
                'accounts/user/list.html',
                {'section': 'people',
                'users': users})

#The user_detail view uses the get_object_or_404() shortcut to retrieve the
# active user with the given username.    
@login_required
def user_detail(request, username):
# The view returns an HTTP 404 response if no active user with the given username is found.
    user = get_object_or_404(User,
                           username=username,
                           is_active=True)

    return render(request,
                 'accounts/user/detail.html',
                 {'section': 'people',
                 'user': user})

# creating the follow and unfollow btn
# You use the intermediary Contact model to create or delete user relationships.
@ajax_required
@require_POST
@login_required #user_follower view is similar to image_likes btn
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_form=request.user,
                                                user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_form=request.user,
                                        user_to=user).delete()
            return JsonResponse({'status': 'ok'})

        except User.DoesNotExist:
            return JsonResponse({'status' : 'error'})
        return JsonResponse({'status': 'error'})


