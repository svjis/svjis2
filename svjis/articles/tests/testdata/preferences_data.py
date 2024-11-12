from ..factories import PreferencesFactory, CompanyFactory


class PreferencesDataMixin:

    @classmethod
    def setUpTestData(cls):
        cls.company = CompanyFactory(name="Testing company", internet_domain="www.test.cz")
        cls.p_fault_notif = PreferencesFactory(
            key="mail.template.fault.notification", value="Uživatel {} vložil novou závadu {}: <br><br><br>{}"
        )
