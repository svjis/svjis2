import factory

from ...models import Preferences


class PreferencesFactory(factory.django.DjangoModelFactory):
    key = factory.Faker("word")
    value = factory.Faker("word")

    class Meta:
        model = Preferences
