from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

'''This is the model we will use to store images bookmarked from
different sites'''
class Image(models.Model):
    # user indicates the User object that bookmarked this image.
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            related_name='images_created',
                            on_delete=models.CASCADE)
#Image model to store the users who
#like an image. We will need a many-to-many relationship in this
#case because a user might like multiple images and each image can
#be liked by multiple users

# related_name allows us to name the relationship from the related object back to
#this one
# many-to-many provides us with a many-to-many manager tht allows us to retreive related objects eg image.users_like.all() or  user.images_liked.all()
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked',
                                        blank=True)
    title = models.CharField(max_length=200) #A title for the image.
    slug = models.SlugField(max_length=200, blank=True) #slug is used for building beautiful SEO-friendly URLs.
    url = models.URLField() #The original URL for this image.
    image = models.ImageField(upload_to='images/%Y/%m/%d/') #the image file
    description = models.TextField(blank=True) #An optional description for the image.
    created = models.DateField(auto_now_add=True, db_index=True) # date and time the object is created ib the db
    # We use db_index=True so that Django creates an index in the
# database for this field.

# The total_likes field will allow you to store the total count of users who like each image
    total_likes = models.PositiveIntegerField(db_index=True,
                                            default=0)
# '''Denormalizing counts is useful when you want to filter or order QuerySets
# by them.'''

    def __str__(self):
        return self.title

#automatically generate the slug field using slugify based on the value of the title field if no slug is provided. 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)

    def get_absolute_url(self):
            return reverse('images:detail', args=[self.id, self.slug])

'''NB:Foreign key
This indicates the User object that bookmarked this
image. This is a foreign key field because it specifies a oneto-
many relationship. A user can post multiple images, but
each image is posted by a single user.'''