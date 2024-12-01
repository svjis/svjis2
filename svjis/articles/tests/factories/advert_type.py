import factory

from ...models import AdvertType


class AdvertTypeFactory(factory.django.DjangoModelFactory):
    description = factory.Faker('sentence', nb_words=6)

    class Meta:
        model = AdvertType
