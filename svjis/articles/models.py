import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Article / Redaction
#####################

class Article(models.Model):
    header = models.CharField(_("Header"), max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(_("Published"), default=False)
    perex = models.TextField(_("Perex (markdown)"))
    body = models.TextField(_("Body (markdown)"))
    menu = models.ForeignKey("ArticleMenu", on_delete=models.CASCADE, null=False, blank=False)
    allow_comments = models.BooleanField(_("Allow comments"), default=False)

    def __str__(self):
        return f"Article: {self.header}"

    @property
    def assets(self):
        return self.articleasset_set.all()

    @property
    def comments(self):
        return self.articlecomment_set.all()

    class Meta:
        ordering = ['-id']
        permissions = (
            ("svjis_view_redaction_menu", "Can view Redaction menu"),
            ("svjis_edit_article", "Can edit Article"),
        )


class ArticleLog(models.Model):
    entry_time = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"ArticleLog: {self.header}"


def article_directory_path(instance, filename):
    return 'articles/{0}/{1}'.format(instance.article.id, filename)


class ArticleAsset(models.Model):
    description = models.CharField(_("Description"), max_length=100)
    file = models.FileField(_("File"), upload_to=article_directory_path)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name=_("Article"))
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Asset: {self.description}"

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super(ArticleAsset, self).delete(*args, **kwargs)

    class Meta:
        ordering = ['-id']


class ArticleComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name=_("Article"))
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    body = models.TextField(_("Body"))

    def __str__(self):
        return f"ArticleComment: {self.description}"

    class Meta:
        ordering = ['-id']
        permissions = (
            ("svjis_add_article_comment", "Can add Article comment"),
        )


class ArticleMenu(models.Model):
    description = models.CharField(_("Description"), max_length=100)
    hide = models.BooleanField(_("Hide"), default=False)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"ArticleMenu: {self.description}"

    @property
    def assets(self):
        return self.asset_set.all()

    class Meta:
        ordering = ['description']
        permissions = (
            ("svjis_edit_article_menu", "Can edit Menu"),
        )


class News(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(_("Published"), default=False)
    body = models.TextField(_("Body"))

    def __str__(self):
        return f"MiniNews: {self.body}"

    class Meta:
        ordering = ['-id']
        permissions = (
            ("svjis_edit_article_news", "Can edit News"),
        )

# Administration
#####################

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    salutation = models.CharField(_("Salutation"), max_length=30, blank=True)
    address = models.CharField(_("Address"),max_length=50, blank=True)
    city = models.CharField(_("City"),max_length=50, blank=True)
    post_code = models.CharField(_("Post code"),max_length=10, blank=True)
    country = models.CharField(_("Country"),max_length=50, blank=True)
    phone = models.CharField(_("Phone"),max_length=30, blank=True)
    show_in_phonelist = models.BooleanField(_("Show in phonelist"), default=False)
    internal_note = models.CharField(_("Internal note"),max_length=250, blank=True)

    def __str__(self):
        return f"UserProfile: {self.user.username}"

    class Meta:
        permissions = (
            ("svjis_view_admin_menu", "Can view Administration menu"),
            ("svjis_edit_admin_users", "Can edit Users"),
            ("svjis_edit_admin_groups", "Can edit Groups"),
            ("svjis_view_personal_menu", "Can view Personal settings menu"),
        )


class MessageQueue(models.Model):
    email = models.CharField(_("E-Mail"), max_length=50, blank=False)
    subject = models.CharField(_("Subject"),max_length=100, blank=False)
    body = models.TextField(_("Body"))
    creation_time = models.DateTimeField(auto_now_add=True)
    sending_time = models.DateTimeField(null=True)
    status = models.SmallIntegerField(null=False)


class ApplicationSetup(models.Model):
    key = models.CharField(_("Key"), max_length=50, blank=False, null=False)
    value = models.CharField(_("Value"), max_length=1000, null=False)
    class Meta:
        permissions = (
            ("svjis_edit_admin_properties", "Can edit Properties"),
        )


class Company(models.Model):
    name = models.CharField(_("Name"), max_length=50, blank=True)
    address = models.CharField(_("Address"), max_length=50, blank=True)
    city = models.CharField(_("City"), max_length=50, blank=True)
    post_code = models.CharField(_("Post code"), max_length=10, blank=True)
    phone = models.CharField(_("Phone"), max_length=30, blank=True)
    email = models.CharField(_("E-Mail"), max_length=50, blank=True)
    registration_no = models.CharField(_("Registration no."), max_length=20, blank=True)
    vat_registration_no = models.CharField(_("VAT Registration no."), max_length=20, blank=True)
    internet_domain = models.CharField(_("Internet domain"), max_length=50, blank=True)
    class Meta:
        permissions = (
            ("svjis_edit_admin_company", "Can edit Company"),
        )


class Buliding(models.Model):
    address = models.CharField(_("Address"), max_length=50, blank=True)
    city = models.CharField(_("City"), max_length=50, blank=True)
    post_code = models.CharField(_("Post code"), max_length=10, blank=True)
    land_registry_no = models.CharField(_("Land Registration no."), max_length=50, blank=True)
    class Meta:
        permissions = (
            ("svjis_edit_admin_building", "Can edit Building"),
        )
