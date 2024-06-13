import factory

from django.contrib.contenttypes.models import ContentType


class ContentTypeFactory(factory.django.DjangoModelFactory):
    app_label = factory.Faker('word')
    model = factory.Faker('word')

    class Meta:
        model = ContentType
        django_get_or_create = ("app_label", "model")
