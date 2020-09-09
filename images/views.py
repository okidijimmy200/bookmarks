from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm

@login_required #prevent access for unauthenticated users.
def image_create(request):
#We expect initial data via GET in order to create an instance of
#the form. This data will consist of the url and title attributes
#of an image from an external website

# data is then posted into our site
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_item = form.save(commit=False) #create new image instance bt prevent the form from being saved in the db using commit=False
            # assign current user to item
            new_item.user = request.user #This is how we can know who uploaded each image.
            new_item.save() #save image object to db
            messages.success(request, 'Image added successfully')

            # redirect to new created item detail view
            return redirect(new_item.get_absolute_url())

    else:
        # build form with data provided by the bookmarket via GET
        form = ImageCreateForm(data=request.GET)

    return render(request, 'images/image/create.html',
                        {'section': 'images',
                        'form': form} )
