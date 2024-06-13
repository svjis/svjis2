import factory

from . import ArticleMenuFactory
from ...models import Article
from .user import UserFactory


class ArticleFactory(factory.django.DjangoModelFactory):
    header = factory.Faker('sentence', nb_words=6)
    slug = factory.Faker('slug')
    author = factory.SubFactory(UserFactory)
    created_date = factory.Faker('date_time')
    published = factory.Faker('boolean')
    perex = factory.Faker('text')
    body = factory.Faker('text')
    menu = factory.SubFactory(ArticleMenuFactory)
    allow_comments = factory.Faker('boolean')
    visible_for_all = factory.Faker('boolean')

    class Meta:
        model = Article

    @factory.post_generation
    def watching_users(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of watching_users were passed in, use them
            for watching_user in extracted:
                self.watching_users.add(watching_user)

    @factory.post_generation
    def visible_for_group(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of visible_for_group were passed in, use them
            for group in extracted:
                self.visible_for_group.add(group)
