from django import forms
from django.contrib.auth.models import User, Group
from . import models


class ArticleMenuForm(forms.ModelForm):
    class Meta:
        model = models.ArticleMenu
        fields = ("description", "hide", "parent",)
        widgets = {
            'description': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'hide': forms.widgets.CheckboxInput(attrs={'class': 'common-input'}),
            'parent': forms.widgets.Select(attrs={'class': 'common-input'}),
        }


class ArticleForm(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ("header", "perex", "body", "menu", "allow_comments", "published",)
        widgets = {
            'header': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'perex': forms.widgets.Textarea(attrs={'class': 'common-textarea', 'rows': '10', 'cols': '80', 'wrap': True}),
            'body': forms.widgets.Textarea(attrs={'class': 'common-textarea', 'rows': '20', 'cols': '80', 'wrap': True}),
            'menu': forms.widgets.Select(attrs={'class': 'common-input'}),
            'allow_comments': forms.widgets.CheckboxInput(attrs={'class': 'common-input'}),
            'published': forms.widgets.CheckboxInput(attrs={'class': 'common-input'}),
        }


class ArticleAssetForm(forms.ModelForm):
    class Meta:
        model = models.ArticleAsset
        fields = ("description", "file",)
        widgets = {
            'description': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'file': forms.widgets.FileInput(attrs={'class': 'common-input', 'size': '50'}),
        }


class NewsForm(forms.ModelForm):
    class Meta:
        model = models.News
        fields = ("body", "published",)
        widgets = {
            'body': forms.widgets.Textarea(attrs={'class': 'common-textarea', 'rows': '20', 'cols': '80', 'wrap': True}),
            'published': forms.widgets.CheckboxInput(attrs={'class': 'common-input'}),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "is_active")
        widgets = {
            'first_name': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'last_name': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'email': forms.widgets.EmailInput(attrs={'class': 'common-input', 'size': '50'}),
            'username': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'is_active': forms.widgets.CheckboxInput(attrs={'class': 'common-input'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = ("salutation", "address", "city", "post_code", "country", "phone", "show_in_phonelist", "internal_note")
        widgets = {
            'salutation': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'address': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'city': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'post_code': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'country': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'phone': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'show_in_phonelist': forms.widgets.CheckboxInput(attrs={'class': 'common-input'}),
            'internal_note': forms.widgets.Textarea(attrs={'class': 'common-textarea', 'rows': '5', 'cols': '40', 'wrap': True}),
        }


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


class MemberModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.first_name} {obj.last_name} ({obj.username})"


class BoardForm(forms.ModelForm):
    member = MemberModelChoiceField(queryset=User.objects.filter(is_active=True))
    class Meta:
        model = models.Board
        fields = ("order", "member", "position")
        widgets = {
            'order': forms.widgets.NumberInput(attrs={'class': 'common-input'}),
            'member': forms.widgets.Select(attrs={'class': 'common-input'}),
            'position': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
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
