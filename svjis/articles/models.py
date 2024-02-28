import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Article(models.Model):
    header = models.CharField(_("Header"), max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(_("Published"), default=False)
    perex = models.TextField(_("Perex (markdown)"))
    body = models.TextField(_("Body (markdown)"))

    def __str__(self):
        return f"Article: {self.header}"

    @property
    def assets(self):
        return self.asset_set.all()

    class Meta:
        ordering = ['-id']


def article_directory_path(instance, filename):
    return 'assets/{0}/{1}'.format(instance.article.id, filename)

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


class ArticleMenu(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(_("Description"), max_length=100)
    hide = models.BooleanField(_("Hide"), default=False)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"ArticleMenu: {self.description}"

    @property
    def assets(self):
        return self.asset_set.all()
