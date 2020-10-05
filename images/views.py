from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, \
                                 PageNotAnInteger
from actions.utils import create_action
import redis
from django.conf import settings

# connect to redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)

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
            create_action(request.user, 'bookmarked image', new_item)
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
    # increment tota image views by 1
# In this view, you use the incr command that increments the value of a given key by
# 1. If the key doesn't exist, the incr command creates it. The incr() method returns
# the final value of the key after performing the operation. total_views = r.incr(f'image:{image.id}:views') increment image ranking by 1
# ------------------------------------------------------------------------------------------
# You store the value in the total_views variable and pass it in the template context and you build the redis key using a notation eg object-type:id:field
    total_views = r.incr(f'image:{image.id}:views')
    # increment image ranking by 1
    r.zincrby('image_ranking', 1, image.id)
    return render(request,
                    'images/image/detail.html',
                    {'section': 'images',
                    'image': image,
                    'total_views': total_views})

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
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'error'})

'''JsonResponse  class provided by Django, which returns an
HTTP response with an application/json content type, converting the given object
into a JSON output'''


# Let's implement an image list view that will handle both standard browser requests
# and AJAX requests, including pagination.
@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # # If page is not an integer deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
        # If the request is AJAX and the page is out of range
        # return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)

    if request.is_ajax():
        return render(request,
                    'images/image/list_ajax.html',
                    {'section':'images', 'images': images} )
    return render(request,
                    'images/image/list.html',
                    {'section': 'images', 'images': images})




