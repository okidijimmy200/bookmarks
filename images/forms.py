from django import forms
from .models import Image

# form to submit new images
class ImageCreateForm(forms.ModelForm): #model form built from image model
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput,
            # We use this widget because we don't want this field to be visible to users.
        }

'''we will not enter URL directly in the form. we will provide them with a JavaScript tool to enable User
choose an image from an external site, and our form will receive its
URL as a parameter.'''