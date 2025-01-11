from ..factories import GroupFactory, UserFactory, PermissionFactory
from .preferences_data import PreferencesDataMixin
from ...utils import generate_password


class UserDataMixin(PreferencesDataMixin):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.g_owner = GroupFactory(
            name="owner",
            permissions=[
                PermissionFactory(codename="svjis_add_article_comment"),
                PermissionFactory(codename="svjis_view_personal_menu"),
                PermissionFactory(codename="svjis_view_phonelist"),
                PermissionFactory(codename="svjis_answer_survey"),
                PermissionFactory(codename="svjis_view_fault_menu"),
                PermissionFactory(codename="svjis_fault_reporter"),
                PermissionFactory(codename="svjis_add_fault_comment"),
                PermissionFactory(codename="svjis_view_adverts_menu"),
                PermissionFactory(codename="svjis_add_advert"),
            ],
        )
        cls.g_board_member = GroupFactory(
            name="board_member",
            permissions=[
                PermissionFactory(codename="svjis_add_article_comment"),
                PermissionFactory(codename="svjis_view_personal_menu"),
                PermissionFactory(codename="svjis_view_phonelist"),
                PermissionFactory(codename="svjis_fault_resolver"),
            ],
        )
        cls.g_vendor = GroupFactory(
            name="vendor",
            permissions=[
                PermissionFactory(codename="svjis_add_article_comment"),
                PermissionFactory(codename="svjis_view_personal_menu"),
                PermissionFactory(codename="svjis_view_fault_menu"),
                PermissionFactory(codename="svjis_fault_reporter"),
                PermissionFactory(codename="svjis_fault_resolver"),
                PermissionFactory(codename="svjis_add_fault_comment"),
            ],
        )
        cls.g_redactor = GroupFactory(
            name="redactor",
            permissions=[
                PermissionFactory(codename="svjis_view_redaction_menu"),
                PermissionFactory(codename="svjis_edit_article"),
                PermissionFactory(codename="svjis_edit_article_menu"),
                PermissionFactory(codename="svjis_edit_survey"),
                PermissionFactory(codename="svjis_edit_article_news"),
            ],
        )
        cls.g_admin = GroupFactory(
            name="admin",
            permissions=[
                PermissionFactory(codename="svjis_view_redaction_menu"),
                PermissionFactory(codename="svjis_edit_article"),
                PermissionFactory(codename="svjis_add_article_comment"),
                PermissionFactory(codename="svjis_edit_article_menu"),
                PermissionFactory(codename="svjis_edit_article_news"),
                PermissionFactory(codename="svjis_view_admin_menu"),
                PermissionFactory(codename="svjis_edit_admin_users"),
                PermissionFactory(codename="svjis_edit_admin_groups"),
                PermissionFactory(codename="svjis_view_personal_menu"),
                PermissionFactory(codename="svjis_edit_admin_preferences"),
                PermissionFactory(codename="svjis_edit_admin_company"),
                PermissionFactory(codename="svjis_edit_admin_building"),
                PermissionFactory(codename="svjis_view_phonelist"),
                PermissionFactory(codename="svjis_view_fault_menu"),
                PermissionFactory(codename="svjis_fault_reporter"),
                PermissionFactory(codename="svjis_fault_resolver"),
                PermissionFactory(codename="svjis_add_fault_comment"),
            ],
        )

        cls.u_jiri_password = generate_password(6)
        cls.u_jiri = UserFactory(
            username="jiri",
            email="jiri@test.cz",
            password=cls.u_jiri_password,
            first_name="Jiří",
            last_name="Brambůrek",
            groups=[cls.g_owner, cls.g_board_member, cls.g_redactor],
        )
        cls.u_peter_password = generate_password(6)
        cls.u_peter = UserFactory(
            username="peter",
            email="peter@test.cz",
            password=cls.u_peter_password,
            first_name="Peter",
            last_name="Nebus",
            groups=[cls.g_owner],
        )
        cls.u_karel_password = generate_password(6)
        cls.u_karel = UserFactory(
            username="karel",
            email="karel@test.cz",
            password=cls.u_karel_password,
            first_name="Karel",
            last_name="Lukáš",
            groups=[cls.g_vendor],
        )
        cls.u_jarda_password = generate_password(6)
        cls.u_jarda = UserFactory(
            username="jarda",
            email="jarda@test.cz",
            password=cls.u_jarda_password,
            first_name="Jaroslav",
            last_name="Beran",
            groups=[cls.g_owner, cls.g_board_member, cls.g_admin],
        )
