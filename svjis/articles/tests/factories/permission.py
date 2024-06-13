import factory

from django.contrib.auth import models

from . import ContentTypeFactory


class PermissionFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("word")
    content_type = factory.SubFactory(ContentTypeFactory, app_label="articles")
    codename = factory.Faker("word")

    class Meta:
        model = models.Permission
        django_get_or_create = ("codename",)
