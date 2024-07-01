from django import forms
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from . import models
from tinymce.widgets import TinyMCE


SELECT_ENTRANCE_TEXT = "Select the entranance (if does it make sense)"


class ArticleMenuForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = models.ArticleMenu.objects.exclude(pk=self.instance.pk)

    class Meta:
        model = models.ArticleMenu
        fields = (
            "description",
            "hide",
            "parent",
        )
        widgets = {
            'description': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'hide': forms.widgets.CheckboxInput(attrs={'class': 'common-input'}),
            'parent': forms.widgets.Select(attrs={'class': 'common-input'}),
        }


class ArticleForm(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ("header", "perex", "body", "menu", "allow_comments", "published", "visible_for_all")
        widgets = {
            'header': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'perex': TinyMCE(
                attrs={'class': 'common-textarea', 'rows': '20', 'cols': '30'},
                mce_attrs={
                    'entity_encoding': 'raw',
                    'height': '350px',
                    'width': '600px',
                },
            ),
            'body': TinyMCE(
                attrs={'class': 'common-textarea', 'rows': '20', 'cols': '30'},
                mce_attrs={
                    'entity_encoding': 'raw',
                    'height': '350px',
                    'width': '600px',
                },
            ),
            'menu': forms.widgets.Select(attrs={'class': 'common-input'}),
            'allow_comments': forms.widgets.CheckboxInput(attrs={'class': 'common-input'}),
            'published': forms.widgets.CheckboxInput(attrs={'class': 'common-input'}),
            'visible_for_all': forms.widgets.CheckboxInput(attrs={'class': 'common-input'}),
        }


class ArticleAssetForm(forms.ModelForm):
    class Meta:
        model = models.ArticleAsset
        fields = (
            "description",
            "file",
        )
        widgets = {
            'description': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'file': forms.widgets.FileInput(attrs={'class': 'common-input', 'size': '50'}),
        }


class NewsForm(forms.ModelForm):
    class Meta:
        model = models.News
        fields = (
            "body",
            "published",
        )
        widgets = {
            'body': forms.widgets.Textarea(
                attrs={'class': 'common-textarea', 'rows': '20', 'cols': '80', 'wrap': True}
            ),
            'published': forms.widgets.CheckboxInput(attrs={'class': 'common-input'}),
        }


class UsefulLinkForm(forms.ModelForm):
    class Meta:
        model = models.UsefulLink
        fields = (
            "header",
            "link",
            "order",
            "published",
        )
        widgets = {
            'published': forms.widgets.CheckboxInput(attrs={'class': 'common-input'}),
        }


class SurveyForm(forms.ModelForm):
    class Meta:
        model = models.Survey
        fields = (
            "description",
            "starting_date",
            "ending_date",
            "published",
        )
        widgets = {
            'description': forms.widgets.Textarea(
                attrs={'class': 'common-textarea', 'rows': '5', 'cols': '80', 'wrap': True}
            ),
            'starting_date': forms.widgets.DateInput(
                format=('%Y-%m-%d'), attrs={'placeholder': 'Select Date', 'type': 'date'}
            ),
            'ending_date': forms.widgets.DateInput(
                format=('%Y-%m-%d'), attrs={'placeholder': 'Select Date', 'type': 'date'}
            ),
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
        fields = (
            "salutation",
            "address",
            "city",
            "post_code",
            "country",
            "phone",
            "show_in_phonelist",
            "internal_note",
        )
        widgets = {
            'salutation': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'address': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'city': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'post_code': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'country': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'phone': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'show_in_phonelist': forms.widgets.CheckboxInput(attrs={'class': 'common-input'}),
            'internal_note': forms.widgets.Textarea(
                attrs={'class': 'common-textarea', 'rows': '5', 'cols': '40', 'wrap': True}
            ),
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
        fields = (
            "key",
            "value",
        )
        widgets = {
            'key': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'value': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
        }


class CompanyForm(forms.ModelForm):
    class Meta:
        model = models.Company
        fields = (
            "name",
            "address",
            "city",
            "post_code",
            "phone",
            "email",
            "registration_no",
            "vat_registration_no",
            "internet_domain",
            "header_picture",
        )
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
            'header_picture': forms.widgets.FileInput(attrs={'class': 'common-input', 'size': '50'}),
        }


class MemberModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.last_name} {obj.first_name} ({obj.username})"


class BoardForm(forms.ModelForm):
    member = MemberModelChoiceField(queryset=User.objects.filter(is_active=True).order_by('last_name'))

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
        model = models.Building
        fields = ("address", "city", "post_code", "land_registry_no")
        widgets = {
            'address': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'city': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'post_code': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'land_registry_no': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
        }


class BuildingEntranceForm(forms.ModelForm):
    class Meta:
        model = models.BuildingEntrance
        fields = ("description", "address")
        widgets = {
            'description': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'address': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
        }


class BuildingUnitTypeModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.description}"


class BuildingEntranceChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.description}, {obj.address}"


class BuildingUnitForm(forms.ModelForm):
    type = BuildingUnitTypeModelChoiceField(queryset=models.BuildingUnitType.objects.all().order_by('description'))
    entrance = BuildingEntranceChoiceField(
        queryset=models.BuildingEntrance.objects.all().order_by('description'),
        required=False,
        help_text=_(SELECT_ENTRANCE_TEXT),
    )

    class Meta:
        model = models.BuildingUnit
        fields = ("type", "entrance", "registration_id", "description", "numerator", "denominator")
        widgets = {
            'type': forms.widgets.Select(attrs={'class': 'common-input'}),
            'entrance': forms.widgets.Select(attrs={'class': 'common-input'}),
            'registration_id': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'description': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'address': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'numerator': forms.widgets.NumberInput(attrs={'class': 'common-input'}),
            'denominator': forms.widgets.NumberInput(attrs={'class': 'common-input'}),
        }


class FaultReportForm(forms.ModelForm):
    entrance = BuildingEntranceChoiceField(
        queryset=models.BuildingEntrance.objects.all().order_by('description'),
        required=False,
        help_text=_(SELECT_ENTRANCE_TEXT),
    )

    class Meta:
        model = models.FaultReport
        fields = (
            "subject",
            "entrance",
            "description",
        )
        widgets = {
            'subject': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '80'}),
            'entrance': forms.widgets.Select(attrs={'class': 'common-input'}),
            'description': forms.widgets.Textarea(
                attrs={'class': 'common-textarea', 'rows': '5', 'cols': '80', 'wrap': True}
            ),
        }


class AssignedUserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.last_name} {obj.first_name}"


class FaultReportEditForm(forms.ModelForm):
    entrance = BuildingEntranceChoiceField(
        queryset=models.BuildingEntrance.objects.all().order_by('description'),
        required=False,
        help_text=_(SELECT_ENTRANCE_TEXT),
    )
    assigned_to_user = AssignedUserChoiceField(
        queryset=User.objects.filter(groups__permissions__codename='svjis_fault_resolver')
        .exclude(is_active=False)
        .distinct()
        .order_by('last_name'),
        required=False,
    )

    class Meta:
        model = models.FaultReport
        fields = ("subject", "entrance", "description", "assigned_to_user", "closed")
        widgets = {
            'subject': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '80'}),
            'entrance': forms.widgets.Select(attrs={'class': 'common-input'}),
            'description': forms.widgets.Textarea(
                attrs={'class': 'common-textarea', 'rows': '5', 'cols': '80', 'wrap': True}
            ),
            'assigned_to_user': forms.widgets.Select(attrs={'class': 'common-input'}),
            'closed': forms.widgets.CheckboxInput(attrs={'class': 'common-input', 'size': '50'}),
        }


class FaultAssetForm(forms.ModelForm):
    class Meta:
        model = models.FaultAsset
        fields = (
            "description",
            "file",
        )
        widgets = {
            'description': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'file': forms.widgets.FileInput(attrs={'class': 'common-input', 'size': '50'}),
        }


class AdvertForm(forms.ModelForm):

    class Meta:
        model = models.Advert
        fields = ("type", "header", "body", "phone", "email", "published")
        widgets = {
            'type': forms.widgets.Select(attrs={'class': 'common-input'}),
            'header': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '80'}),
            'body': forms.widgets.Textarea(
                attrs={'class': 'common-textarea', 'rows': '5', 'cols': '80', 'wrap': True}
            ),
            'phone': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'email': forms.widgets.EmailInput(attrs={'class': 'common-input', 'size': '50'}),
            'published': forms.widgets.CheckboxInput(attrs={'class': 'common-input'}),
        }


class AdvertAssetForm(forms.ModelForm):
    class Meta:
        model = models.AdvertAsset
        fields = (
            "description",
            "file",
        )
        widgets = {
            'description': forms.widgets.TextInput(attrs={'class': 'common-input', 'size': '50'}),
            'file': forms.widgets.FileInput(attrs={'class': 'common-input', 'size': '50'}),
        }
