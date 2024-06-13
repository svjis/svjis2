import factory

from ...models import ArticleMenu


class ArticleMenuFactory(factory.django.DjangoModelFactory):
    description = factory.Faker('sentence', nb_words=6)
    hide = False
    parent = factory.LazyAttribute(lambda x: ArticleMenuFactory(parent=None))

    class Meta:
        model = ArticleMenu
