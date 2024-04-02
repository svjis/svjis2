from django.core.management.base import BaseCommand
import mypwd
from firebird.driver import connect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group, User
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
    ORDER BY r.ID
    '''
    cur = cnn.cursor()
    cur.execute(SELECT)
    for row in cur:
        i = models.BuildingUnit.objects.filter(description=row[4]).count()
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


def migrate_users(cnn):
    SELECT = '''
    SELECT r.ID, r.COMPANY_ID, r.FIRST_NAME, r.LAST_NAME, r.SALUTATION, r.ADDRESS,
    r.CITY, r.POST_CODE, r.COUNTRY, r.FIXED_PHONE, r.CELL_PHONE, r.E_MAIL,
    r.LOGIN, r."PASSWORD", r.ENABLED, r.SHOW_IN_PHONELIST, r.LANGUAGE_ID,
    r.PASSWORD_HASH, r.PASSWORD_SALT, r.INTERNAL_NOTE, r.PERM_LOGIN_HASH,
    r.PERM_LOGIN_EXPIRES
    FROM "USER" r
    WHERE r.COMPANY_ID = 1
    ORDER BY r.ID
    '''
    cur = cnn.cursor()
    cur.execute(SELECT)
    for row in cur:
        i = User.objects.filter(username=row[12], first_name=row[2], last_name=row[3], email=row[11], is_active=(row[14] != 0)).count()
        if i == 0:
            print(f"creating user {row[2]} {row[3]}")
            obj = User(username=row[12], first_name=row[2], last_name=row[3], email=row[11], is_active=(row[14] != 0), is_staff=False, is_superuser=False)
            obj.save()
            pobj = models.UserProfile(salutation=row[4], address=row[5], city=row[6], post_code=row[7], country=row[8], phone=row[10], show_in_phonelist=(row[15] != 0), internal_note=row[19])
            obj.userprofile = pobj
            obj.userprofile.save()

        else:
            print(f"user {row[2]} {row[3]} already exists")
    cnn.commit()

    SELECT = '''
    SELECT u.LOGIN, u.FIRST_NAME, u.LAST_NAME, u.E_MAIL, u.ENABLED, o.DESCRIPTION
    FROM USER_HAS_ROLE r
    LEFT JOIN "USER" u ON u.ID = r.USER_ID
    LEFT JOIN "ROLE" o ON o.ID = r.ROLE_ID
    WHERE u.COMPANY_ID = 1
    '''
    cur = cnn.cursor()
    cur.execute(SELECT)
    for row in cur:
        i = User.objects.filter(username=row[0], first_name=row[1], last_name=row[2], email=row[3], is_active=(row[4] != 0)).count()
        if i == 1:
            print(f"creating user group for {row[1]} {row[2]}")
            u = User.objects.filter(username=row[0], first_name=row[1], last_name=row[2], email=row[3], is_active=(row[4] != 0))[0]
            g = Group.objects.filter(name=row[5])[0]
            u.groups.add(g)
        else:
            print(f"user {row[1]} {row[2]} does not exist")
    cnn.commit()

    SELECT = '''
    SELECT u.LOGIN, u.FIRST_NAME, u.LAST_NAME, u.E_MAIL, u.ENABLED, b.DESCRIPTION
    FROM USER_HAS_BUILDING_UNIT r
    LEFT JOIN "USER" u on u.ID = r.USER_ID
    LEFT JOIN BUILDING_UNIT b on b.ID = r.BUILDING_UNIT_ID
    WHERE u.COMPANY_ID = 1
    '''
    cur = cnn.cursor()
    cur.execute(SELECT)
    for row in cur:
        i = User.objects.filter(username=row[0], first_name=row[1], last_name=row[2], email=row[3], is_active=(row[4] != 0)).count()
        if i == 1:
            print(f"creating user unit for {row[1]} {row[2]}")
            u = User.objects.filter(username=row[0], first_name=row[1], last_name=row[2], email=row[3], is_active=(row[4] != 0))[0]
            b = models.BuildingUnit.objects.filter(description=row[5])[0]
            u.buildingunit_set.add(b)
        else:
            print(f"user {row[1]} {row[2]} does not exist")
    cnn.commit()


def migrate_board(cnn):
    SELECT = '''
    SELECT u.LOGIN, u.FIRST_NAME, u.LAST_NAME, u.E_MAIL, u.ENABLED, t.DESCRIPTION, t.ID
    FROM BOARD_MEMBER r
    LEFT JOIN "USER" u on u.ID = r.USER_ID
    LEFT JOIN BOARD_MEMBER_TYPE t on t.ID = r.BOARD_MEMBER_TYPE_ID
    WHERE u.COMPANY_ID = 1
    '''
    cur = cnn.cursor()
    cur.execute(SELECT)
    for row in cur:
        i = User.objects.filter(username=row[0], first_name=row[1], last_name=row[2], email=row[3], is_active=(row[4] != 0)).count()
        if i == 1:
            print(f"creating board for {row[1]} {row[2]}")
            u = User.objects.filter(username=row[0], first_name=row[1], last_name=row[2], email=row[3], is_active=(row[4] != 0))[0]
            obj = models.Board(company_id=1, order=row[6], member=u, position=row[5])
            obj.save()
        else:
            print(f"user {row[1]} {row[2]} does not exist")
    cnn.commit()


def migrate_menu(cnn):
    SELECT = '''
    SELECT r.ID, r.COMPANY_ID, r.PARENT_ID, r.DESCRIPTION, r.HIDE
    FROM MENU_TREE r
    WHERE r.COMPANY_ID = 1
    '''
    cur = cnn.cursor()
    cur.execute(SELECT)
    for row in cur:
        i = models.ArticleMenu.objects.filter(description=row[3]).count()
        if i == 0:
            print(f"creating menu {row[3]}")
            obj = models.ArticleMenu(description=row[3], hide=(row[4] != 0))
            obj.save()
        else:
            print(f"menu {row[3]} already exists")
    cnn.commit()


def migrate_articles(cnn):
    SELECT = '''
    SELECT r.ID, r.COMPANY_ID, m.DESCRIPTION, r.LANGUAGE_ID, r.HEADER,
    r.DESCRIPTION, r."BODY", u.FIRST_NAME, u.LAST_NAME, u.LOGIN, r.CREATION_DATE, r.PUBLISHED,
    r.COMMENTS_ALLOWED
    FROM ARTICLE r
    LEFT JOIN MENU_TREE m on m.ID = r.MENU_NODE_ID
    LEFT JOIN "USER" u on u.ID = r.CREATED_BY_USER_ID
    WHERE r.COMPANY_ID = 1
    ORDER BY r.ID
    '''
    cur = cnn.cursor()
    cur.execute(SELECT)
    for row in cur:
        i = models.Article.objects.filter(header=row[4], created_date=row[10]).count()
        if i == 0:
            print(f"creating article {row[4]}")
            u = User.objects.filter(username=row[9], first_name=row[7], last_name=row[8])[0]
            m = models.ArticleMenu.objects.filter(description=row[2])[0]
            obj = models.Article(header=row[4], author=u, published=(row[11] != 0), perex=row[5], body=row[6], menu=m, allow_comments=(row[12] != 0))
            obj.save()
            obj.created_date=row[10]
            obj.save()

        else:
            print(f"article {row[4]} already exists")
    cnn.commit()


def migrate_article_permission(cnn):
    SELECT = '''
    SELECT a.HEADER, a.CREATION_DATE, o.DESCRIPTION
    FROM ARTICLE_IS_VISIBLE_TO_ROLE r
    LEFT JOIN ARTICLE a on a.ID = r.ARTICLE_ID
    LEFT JOIN "ROLE" o on o.ID = r.ROLE_ID
    WHERE a.COMPANY_ID = 1
    '''
    cur = cnn.cursor()
    cur.execute(SELECT)
    for row in cur:
        print(f"creating article permission for {row[0]}")
        a = models.Article.objects.filter(header=row[0], created_date=row[1])[0]
        g = Group.objects.filter(name=row[2])[0]
        a.visible_for_group.add(g)
        if row[2] == 'Nepřihlášený uživatel':
            a.visible_for_all = True
            a.save()
    cnn.commit()


def migrate_article_comment(cnn):
    SELECT = '''
    SELECT r.INSERTION_TIME, r."BODY", a.HEADER, a.CREATION_DATE, u.FIRST_NAME, u.LAST_NAME, u.LOGIN
    FROM TABLE ARTICLE_COMMENT r
    LEFT JOIN ARTICLE a on a.ID = r.ARTICLE_ID
    LEFT JOIN "USER" u on u.ID = r.USER_ID
    WHERE a.COMPANY_ID = 1
    ORDER BY r.ID
    '''
    cur = cnn.cursor()
    cur.execute(SELECT)
    for row in cur:
        print(f"creating article comment for {row[2]}")
        a = models.Article.objects.filter(header=row[2], created_date=row[3])[0]
        u = User.objects.filter(username=row[6], first_name=row[4], last_name=row[5])[0]
        obj = models.ArticleComment(article=a, author=u, body=row[1])
        obj.save()
        obj.created_date = row[0]
        obj.save()
    cnn.commit()


def migrate_article_asset(cnn):
    SELECT = '''
    SELECT r.UPLOAD_TIME, r.FILENAME, a.HEADER, a.CREATION_DATE, u.FIRST_NAME, u.LAST_NAME, u.LOGIN, r."DATA"
    FROM TABLE ARTICLE_ATTACHMENT r
    LEFT JOIN ARTICLE a on a.ID = r.ARTICLE_ID
    LEFT JOIN "USER" u on u.ID = r.USER_ID
    WHERE a.COMPANY_ID = 1
    ORDER BY r.ID
    '''
    cur = cnn.cursor()
    cur.execute(SELECT)
    for row in cur:
        print(f"creating article attachment for {row[2]}")
        a = models.Article.objects.filter(header=row[2], created_date=row[3])[0]
        obj = models.ArticleAsset(description='', article=a)
        obj.file.save(row[1], row[7])
        obj.save()
        obj.created_date = row[0]
        obj.save()
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
        migrate_users(self.cnn)
        migrate_board(self.cnn)
        migrate_menu(self.cnn)
        migrate_articles(self.cnn)
        migrate_article_permission(self.cnn)
        migrate_article_comment(self.cnn)
        migrate_article_asset(self.cnn)
        self.cnn.close()
