from ..factories import PreferencesFactory, CompanyFactory, AdvertTypeFactory


class PreferencesDataMixin:

    @classmethod
    def setUpTestData(cls):

        cls.company = CompanyFactory(name="Testing company", internet_domain="www.test.cz")

        cls.advert_types = [
            AdvertTypeFactory(description="Koupím"),
            AdvertTypeFactory(description="Prodám"),
            AdvertTypeFactory(description="Ostatní"),
        ]

        cls.p_fault_notif = PreferencesFactory(
            key="mail.template.fault.notification", value="Uživatel {} vložil novou závadu {}: <br><br><br>{}"
        )
        cls.p_fault_assigned = PreferencesFactory(
            key="mail.template.fault.assigned", value="Uživatel {} vám přiřadil tiket {}: <br><br><br>{}"
        )
