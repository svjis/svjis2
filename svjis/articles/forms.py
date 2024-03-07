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


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "is_active")

    widgets = {
        'first_name': forms.TextInput(attrs={'class': 'common-input'}),
        'last_name': forms.TextInput(attrs={'class': 'common-input'}),
        'username': forms.TextInput(attrs={'class': 'common-input'}),
        'email': forms.EmailInput(attrs={'class': 'common-input'}),
    }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = ("salutation", "address", "city", "post_code", "country", "phone", "show_in_phonelist", "internal_note")

    widgets = {
        'salutation': forms.TextInput(attrs={'class': 'common-input'}),
        'address': forms.TextInput(attrs={'class': 'common-input'}),
        'city': forms.TextInput(attrs={'class': 'common-input'}),
        'post_code': forms.TextInput(attrs={'class': 'common-input'}),
        'country': forms.TextInput(attrs={'class': 'common-input'}),
        'phone': forms.TextInput(attrs={'class': 'common-input'}),
        'show_in_phonelist': forms.CheckboxInput(attrs={'class': 'common-input'}),
        'internal_note': forms.Textarea(attrs={'class': 'common-input'}),
    }


class GroupEditForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ("name",)
