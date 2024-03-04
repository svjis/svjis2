from django import forms
from django.contrib.auth import get_user_model
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


class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = models.ArticleComment
        fields = ("body",)


class NewsForm(forms.ModelForm):
    class Meta:
        model = models.News
        fields = ("body", "published",)


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "username",)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email",)
