from django import forms


class ArticleMenu(forms.Form):
    description = forms.CharField(max_length=100)
    hide = forms.BooleanField(required=False)
