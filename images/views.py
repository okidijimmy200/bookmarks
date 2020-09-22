from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required

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

# to display an image
def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request,
                    'images/image/detail.html',
                    {'section': 'images',
                    'image': image})

@ajax_required
# view for users to like/unlike images
@login_required
# require_POST decorator returns an HttpResponseNotAllowed object when  HTTP request is not done via POST. This way, you only allow POST requests for this view
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'error'})

'''JsonResponse  class provided by Django, which returns an
HTTP response with an application/json content type, converting the given object
into a JSON output'''


