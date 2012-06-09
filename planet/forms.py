from django import forms

class BlogForm(forms.Form):
    author = forms.CharField()
    name = forms.CharField()
    feed = forms.URLField()

