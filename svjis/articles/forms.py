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


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = ("salutation", "address", "city", "post_code", "country", "phone", "show_in_phonelist", "internal_note")


class PersonalUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class PersonalUserProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = ("salutation", "address", "city", "post_code", "country", "phone", "show_in_phonelist")


class GroupEditForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ("name",)


class ApplicationSetupForm(forms.ModelForm):
    key = forms.CharField(max_length=50)
    key.widget.attrs.update({'class': 'common-input', 'id': 'key-input'})
    value = forms.CharField(max_length=1000)
    value.widget.attrs.update({'class': 'common-input', 'id': 'key-input'})

    class Meta:
        model = models.ApplicationSetup
        fields = ("key", "value",)
