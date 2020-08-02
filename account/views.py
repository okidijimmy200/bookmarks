from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required


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