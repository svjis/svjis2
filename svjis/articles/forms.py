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
        widgets = {
            'first_name': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'last_name': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'email': forms.widgets.EmailInput(attrs={'class': 'common-input', 'size': '50'}),
        }


class PersonalUserProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = ("salutation", "address", "city", "post_code", "country", "phone", "show_in_phonelist")
        widgets = {
            'salutation': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'address': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'city': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'post_code': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'country': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'phone': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'show_in_phonelist': forms.widgets.CheckboxInput(attrs={'class': 'common-input', 'size': '50'}),
        }


class GroupEditForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ("name",)
        widgets = {
            'name': forms.widgets.TextInput(attrs={'class': 'common-input'}),
        }


class PreferencesForm(forms.ModelForm):
    class Meta:
        model = models.Preferences
        fields = ("key", "value",)
        widgets = {
            'key': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'value': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
        }


class CompanyForm(forms.ModelForm):
    class Meta:
        model = models.Company
        fields = ("name", "address", "city", "post_code", "phone", "email", "registration_no", "vat_registration_no", "internet_domain")
        widgets = {
            'name': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'address': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'city': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'post_code': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'phone': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'email': forms.widgets.EmailInput(attrs={'class': 'common-input', 'size': '50'}),
            'registration_no': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'vat_registration_no': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'internet_domain': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
        }


class BuildingForm(forms.ModelForm):
    class Meta:
        model = models.Buliding
        fields = ("address", "city", "post_code", "land_registry_no")
        widgets = {
            'address': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'city': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'post_code': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'land_registry_no': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
        }
