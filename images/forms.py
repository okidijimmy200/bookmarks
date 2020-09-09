from django import forms
from .models import Image
from urllib import request #Python urllib module to download the image
from django.core.files.base import ContentFile
from django.utils.text import slugify

# form to submit new images
class ImageCreateForm(forms.ModelForm): #model form built from image model
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput,
            # We use this widget because we don't want this field to be visible to users.
        }

    # verifying whether the image URL is valid
    def clean_url(self):
        url = self.cleaned_data['url'] #get the value of the url field
        valid_exension = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower() #split the URL to get valid extensions
        if extension not in valid_exension:
            raise forms.ValidationError('The given URL does not '\
                                        'match valid image extension')

        return url
# we will also need to download the image file and save it.
# --we overide the default sace method keeping parameters required by modelForm
    def save(self, force_insert=False,
            force_update=False,commit=True):
# We create a new image instance by calling the save() method of
# the form with commit=False.
        image = super(ImageCreateForm, self).save(commit=False)
# We get the URL from the cleaned_data dictionary of the form.
        image_url = self.cleaned_data['url']
# We generate the image name by combining the image title slug
# with the original file extension.
        image_name = '{}.{}'.format(slugify(image.title),
                    image_url.rsplit('.', 1)[1].lower())

        # download image from the given URL
        response = request.urlopen(image_url)
# passing it a ContentFile object that is instantiated with the downloaded file
# content.
        image.image.save(image_name, ContentFile(response.read()),
                        save=False)
# We also pass the save=False parameter to avoid
# saving the object to the database, yet.


# In order to maintain the same behavior as the save() method
# we override, we save the form to the database only when the
# commit parameter is True.
        if commit:
            image.save()
        return image

'''we will not enter URL directly in the form. we will provide them with a JavaScript tool to enable User
choose an image from an external site, and our form will receive its
URL as a parameter.'''