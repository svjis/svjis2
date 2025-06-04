import factory

from .user import UserFactory
from ...models import FaultReport


class FaultReportFactory(factory.django.DjangoModelFactory):
    subject = factory.Faker('sentence', nb_words=3)
    slug = factory.Faker('slug')
    description = factory.Faker('text')
    created_date = factory.Faker('date_time')
    created_by_user = factory.SubFactory(UserFactory)
    assigned_to_user = factory.SubFactory(UserFactory)
    closed = factory.Faker('boolean')

    class Meta:
        model = FaultReport
