from django import forms
from django.contrib.auth.models import User, Group
from . import models


class ArticleMenuForm(forms.ModelForm):
    class Meta:
        model = models.ArticleMenu
        fields = ("description", "hide", "parent",)


class ArticleForm(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ("header", "perex", "body", "menu", "allow_comments", "published",)


class ArticleAssetForm(forms.ModelForm):
    class Meta:
        model = models.ArticleAsset
        fields = ("description", "file",)


class NewsForm(forms.ModelForm):
    class Meta:
        model = models.News
        fields = ("body", "published",)


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username",)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email",)

class GroupEditForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ("name",)
