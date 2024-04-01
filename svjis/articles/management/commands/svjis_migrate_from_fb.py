from django.core.management.base import BaseCommand
import mypwd
from firebird.driver import connect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from articles import models



def migrate_company(cnn):
    SELECT = '''
    SELECT r.ID, r."NAME", r.ADDRESS, r.CITY, r.POST_CODE, r.PHONE, r.FAX, r.E_MAIL,
    r.REGISTRATION_NO, r.VAT_REGISTRATION_NO, r.DATABASE_CREATION_DATE,
    r.INTERNET_DOMAIN, r.PICTURE_CONTENT_TYPE, r.PICTURE_FILENAME,
    r.PICTURE_DATA
    FROM COMPANY r
    WHERE r.ID = 1
    '''
    cur = cnn.cursor()
    cur.execute(SELECT)
    for row in cur:
        instance, _created = models.Company.objects.get_or_create(pk=1)
        instance.name = row[1]
        instance.address = row[2]
        instance.city = row[3]
        instance.post_code = row[4]
        instance.email = row[7]
        instance.registration_no = row[8]
        instance.internet_domain = row[11]
        instance.save()
    cnn.commit()


def migrate_building(cnn):
    SELECT = '''
    SELECT r.ID, r.COMPANY_ID, r.ADDRESS, r.CITY, r.POST_CODE, r.REGISTRATION_ID
    FROM BUILDING r
    WHERE r.COMPANY_ID = 1
    '''
    cur = cnn.cursor()
    cur.execute(SELECT)
    for row in cur:
        instance, _created = models.Building.objects.get_or_create(pk=1)
        instance.address = row[2]
        instance.city = row[3]
        instance.post_code = row[4]
        instance.land_registry_no = row[5]
        instance.save()
    cnn.commit()


def migrate_building_entrances(cnn):
    SELECT = '''
    SELECT r.ID, r.BUILDING_ID, r.DESCRIPTION, r.ADDRESS
    FROM BUILDING_ENTRANCE r
    WHERE r.BUILDING_ID = 1
    '''
    cur = cnn.cursor()
    cur.execute(SELECT)
    for row in cur:
        i = models.BuildingEntrance.objects.filter(description=row[2]).count()
        if i == 0:
            print(f"creating entrance {row[2]}")
            obj = models.BuildingEntrance(building_id=1, description=row[2], address=row[3])
            obj.save()
        else:
            print(f"entrance {row[2]} already exists")
    cnn.commit()


def migrate_building_units(cnn):
    SELECT = '''
    SELECT r.ID, r.BUILDING_ID, t.DESCRIPTION, r.REGISTRATION_ID,
    r.DESCRIPTION, r.NUMERATOR, r.DENOMINATOR
    FROM BUILDING_UNIT r
    LEFT JOIN BUILDING_UNIT_TYPE t on r.BUILDING_UNIT_TYPE_ID = t.ID
    WHERE r.BUILDING_ID = 1
    '''
    cur = cnn.cursor()
    cur.execute(SELECT)
    for row in cur:
        i = models.BuildingUnit.objects.filter(description=row[2]).count()
        if i == 0:
            print(f"creating unit {row[4]}")
            utype = models.BuildingUnitType.objects.filter(description=row[2])[0]
            obj = models.BuildingUnit(building_id=1, type=utype, registration_id=row[3], description=row[4], numerator=row[5], denominator=row[6])
            ent = row[4][:2]
            enti = models.BuildingEntrance.objects.filter(description=ent).count()
            if enti == 1:
                obj.entrance = models.BuildingEntrance.objects.filter(description=ent)[0]
            obj.save()
        else:
            print(f"unit {row[2]} already exists")
    cnn.commit()


def migrate_groups(cnn):
    SELECT = 'SELECT r.ID, r.DESCRIPTION FROM "ROLE" r where r.COMPANY_ID = 1'
    cur = cnn.cursor()
    cur.execute(SELECT)
    for (id, description) in cur:
        i = Group.objects.filter(name=description).count()
        if i == 0:
            print(f"creating group {description}")
            gobj = Group(name=description)
            gobj.save()
        else:
            print(f"group {description} already exists")
    cnn.commit()


# https://firebird-driver.readthedocs.io/en/latest/getting-started.html#installation
class Command(BaseCommand):
    help = "Migrate from fb"
    cnn = None

    def handle(self, *args, **options):
        db_login, db_password, db_database = mypwd.get_values("svjis-fb", ["login", "password", "database"])
        self.cnn = connect(db_database, user=db_login, password=db_password)

        migrate_company(self.cnn)
        migrate_building(self.cnn)
        migrate_building_entrances(self.cnn)
        migrate_building_units(self.cnn)
        migrate_groups(self.cnn)
        self.cnn.close()
