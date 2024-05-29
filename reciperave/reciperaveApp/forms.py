from django import forms
from django.forms import CharField
from django.models import upload

class pform(forms.Form):
    recipe_name = forms.CharField(max_length=20)
    photo_video = forms.FileField()
    class Meta:
        model = upload
        fields = ['uid', 'recipe_name', 'total_time', 'dishType', 'description', 'photo_video', 'instruction']