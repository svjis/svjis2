from ..factories import ArticleMenuFactory, ArticleFactory
from .user_data import UserDataMixin


class ArticleDataMixin(UserDataMixin):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.menu_docs = ArticleMenuFactory(description="Documents")

        cls.article_not_published = ArticleFactory(
            header='Not Published',
            menu=cls.menu_docs,
            author=cls.u_jiri,
            published=False,
            visible_for_all=True,
        )
        cls.article_for_no_one = ArticleFactory(
            header='For no one',
            menu=cls.menu_docs,
            author=cls.u_jiri,
            published=True,
            visible_for_all=False,
        )
        cls.article_for_all = ArticleFactory(
            header='For All',
            menu=cls.menu_docs,
            author=cls.u_jiri,
            published=True,
            visible_for_all=True,
        )
        cls.article_for_owners = ArticleFactory(
            header='For Owners',
            menu=cls.menu_docs,
            author=cls.u_jiri,
            published=True,
            visible_for_all=False,
            visible_for_group=[cls.g_owner],
        )
        cls.article_for_owners_and_board = ArticleFactory(
            header='For Owners and Board',
            menu=cls.menu_docs,
            author=cls.u_jiri,
            published=True,
            visible_for_all=False,
            visible_for_group=[cls.g_owner, cls.g_board_member],
        )
        cls.article_for_board = ArticleFactory(
            header='For Board',
            menu=cls.menu_docs,
            author=cls.u_jiri,
            published=True,
            visible_for_all=False,
            visible_for_group=[cls.g_board_member],
        )
