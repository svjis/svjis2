import factory

from ...models import Company


class CompanyFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("word")
    address = factory.Faker("word")
    city = factory.Faker("word")
    post_code = factory.Faker("word")
    phone = factory.Faker("word")
    email = factory.Faker("word")
    registration_no = factory.Faker("word")
    vat_registration_no = factory.Faker("word")
    internet_domain = factory.Faker("word")

    class Meta:
        model = Company
