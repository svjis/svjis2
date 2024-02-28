from django import forms
from . import models


# class ArticleMenuForm(forms.Form):
#     description = forms.CharField(max_length=100)
#     hide = forms.BooleanField(required=False)


class ArticleMenuForm(forms.ModelForm):
    class Meta:
        model = models.ArticleMenu
        fields = ("description", "hide", "parent")


class ArticleForm(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ("header", "perex", "body", "menu", "published")
