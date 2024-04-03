from django.core.management.base import BaseCommand
import mypwd
import io
from firebird.driver import connect, driver_config
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
        i = models.Article.objects.filter(header=row[4], created_date=row[10], published=(row[11] != 0)).count()
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
    SELECT a.HEADER, a.CREATION_DATE, o.DESCRIPTION, a.PUBLISHED
    FROM ARTICLE_IS_VISIBLE_TO_ROLE r
    LEFT JOIN ARTICLE a on a.ID = r.ARTICLE_ID
    LEFT JOIN "ROLE" o on o.ID = r.ROLE_ID
    WHERE a.COMPANY_ID = 1
    '''
    cur = cnn.cursor()
    cur.execute(SELECT)
    for row in cur:
        print(f"creating article permission for {row[0]}")
        a = models.Article.objects.filter(header=row[0], created_date=row[1], published=(row[3] != 0))[0]
        g = Group.objects.filter(name=row[2])[0]
        a.visible_for_group.add(g)
        if row[2] == 'Nepřihlášený uživatel':
            a.visible_for_all = True
            a.save()
    cnn.commit()


def migrate_article_comment(cnn):
    SELECT = '''
    SELECT r.INSERTION_TIME, r."BODY", a.HEADER, a.CREATION_DATE, u.FIRST_NAME, u.LAST_NAME, u.LOGIN, a.PUBLISHED
    FROM ARTICLE_COMMENT r
    LEFT JOIN ARTICLE a on a.ID = r.ARTICLE_ID
    LEFT JOIN "USER" u on u.ID = r.USER_ID
    WHERE a.COMPANY_ID = 1
    ORDER BY r.ID
    '''
    cur = cnn.cursor()
    cur.execute(SELECT)
    for row in cur:
        print(f"creating article comment for {row[2]}")
        a = models.Article.objects.filter(header=row[2], created_date=row[3], published=(row[7] != 0))[0]
        u = User.objects.filter(username=row[6], first_name=row[4], last_name=row[5])[0]
        obj = models.ArticleComment(article=a, author=u, body=row[1])
        obj.save()
        obj.created_date = row[0]
        obj.save()
    cnn.commit()


def migrate_article_asset(cnn):
    SELECT = '''
    SELECT r.UPLOAD_TIME, r.FILENAME, a.HEADER, a.CREATION_DATE, u.FIRST_NAME, u.LAST_NAME, u.LOGIN, r."DATA", a.PUBLISHED
    FROM ARTICLE_ATTACHMENT r
    LEFT JOIN ARTICLE a on a.ID = r.ARTICLE_ID
    LEFT JOIN "USER" u on u.ID = r.USER_ID
    WHERE a.COMPANY_ID = 1
    ORDER BY r.ID
    '''
    cur = cnn.cursor()
    cur.execute(SELECT)
    for row in cur:
        print(f"creating article attachment for {row[2]}")
        a = models.Article.objects.filter(header=row[2], created_date=row[3], published=(row[8] != 0))[0]
        obj = models.ArticleAsset(description='', article=a)
        data = row[7]
        obj.file.save(row[1], io.BytesIO(data))
        obj.save()
        obj.created_date = row[0]
        obj.save()
    cnn.commit()


def migrate_article_watching(cnn):
    SELECT = '''
    SELECT a.HEADER, a.CREATION_DATE, u.FIRST_NAME, u.LAST_NAME, u.LOGIN, a.PUBLISHED
    FROM ARTICLE_WATCHING r
    LEFT JOIN ARTICLE a on a.ID = r.ARTICLE_ID
    LEFT JOIN "USER" u on u.ID = r.USER_ID
    WHERE a.COMPANY_ID = 1
    '''
    cur = cnn.cursor()
    cur.execute(SELECT)
    for row in cur:
        print(f"creating article watching for {row[0]} and {row[2]} {row[3]}")
        a = models.Article.objects.filter(header=row[0], created_date=row[1], published=(row[5] != 0))[0]
        u = User.objects.filter(username=row[4], first_name=row[2], last_name=row[3])[0]
        a.watching_users.add(u)
    cnn.commit()


def migrate_news(cnn):
    SELECT = '''
    SELECT r.NEWS_TIME, r."BODY", r.PUBLISHED, u.FIRST_NAME, u.LAST_NAME, u.LOGIN
    FROM MINI_NEWS r
    LEFT JOIN "USER" u on u.ID = r.CREATED_BY_USER_ID
    WHERE r.COMPANY_ID = 1
    '''
    cur = cnn.cursor()
    cur.execute(SELECT)
    for row in cur:
        i = models.News.objects.filter(body=row[1]).count()
        if i == 0:
            print(f"creating news {row[1]}")
            u = User.objects.filter(username=row[5], first_name=row[3], last_name=row[4])[0]
            obj = models.News(author=u, published=(row[2] != 0), body=row[1])
            obj.save()
            obj.created_date=row[0]
            obj.save()
        else:
            print(f"news {row[1]} already exists")
    cnn.commit()


def migrate_survey(cnn):
    SELECT = '''
    SELECT r.DESCRIPTION, r.STARTING_DATE, r.ENDING_DATE, r.ENABLED, u.FIRST_NAME, u.LAST_NAME, u.LOGIN, r.ID
    FROM INQUIRY r
    LEFT JOIN "USER" u on u.ID = r.USER_ID
    WHERE r.COMPANY_ID = 1
    '''
    cur = cnn.cursor()
    cur.execute(SELECT)
    for row in cur:
        i = models.Survey.objects.filter(description=row[0]).count()
        if i == 0:
            print(f"creating survey {row[0]}")
            u = User.objects.filter(username=row[6], first_name=row[4], last_name=row[5])[0]

            fromd = row[1]
            fromd = fromd.date()
            tod = row[2]
            tod = tod.date()

            obj = models.Survey(author=u, description=row[0], starting_date=fromd, ending_date=tod, published=(row[3] != 0))
            obj.save()

            SELECT1 = '''
            SELECT r.DESCRIPTION, r.ID
            FROM INQUIRY_OPTION r
            WHERE r.INQUIRY_ID =
            '''
            cur1 = cnn.cursor()
            cur1.execute(SELECT1 + str(row[7]))
            for row1 in cur1:
                obj1 = models.SurveyOption(description=row1[0], survey=obj)
                obj1.save()

                SELECT2 = '''
                SELECT r.VOTING_TIME, u.FIRST_NAME, u.LAST_NAME, u.LOGIN
                FROM INQUIRY_VOTING_LOG r
                LEFT JOIN "USER" u on u.ID = r.USER_ID
                WHERE r.INQUIRY_OPTION_ID = {}
                ORDER BY r.ID
                '''
                cur2 = cnn.cursor()
                cur2.execute(SELECT2.replace('{}', str(row1[1])))
                for row2 in cur2:
                    u = User.objects.filter(username=row2[3], first_name=row2[1], last_name=row2[2])[0]
                    obj2 = models.SurveyAnswerLog(survey=obj, option=obj1, user=u)
                    obj2.save()
                    obj2.time = row2[0]
                    obj2.save()
                cur2.close()
            cur1.close()

        else:
            print(f"survey {row[0]} already exists")
    cnn.commit()


def migrate_fault_report(cnn):
    SELECT = '''
    SELECT r.SUBJECT, r.DESCRIPTION, r.CREATION_DATE, r.CLOSED, cr.FIRST_NAME, cr.LAST_NAME, cr.LOGIN, ass.FIRST_NAME, ass.LAST_NAME, ass.LOGIN, e.DESCRIPTION, r.ID
    FROM FAULT_REPORT r
    LEFT JOIN "USER" cr on cr.ID = r.CREATED_BY_USER_ID
    LEFT JOIN "USER" ass on ass.ID = r.ASSIGNED_TO_USER_ID
    LEFT JOIN BUILDING_ENTRANCE e on e.ID = r.BUILDING_ENTRANCE_ID
    WHERE r.COMPANY_ID = 1
    ORDER BY r.ID
    '''
    cur = cnn.cursor()
    cur.execute(SELECT)
    for row in cur:
        i = models.FaultReport.objects.filter(subject=row[0], description=row[1], created_date=row[2]).count()
        if i == 0:
            print(f"creating fault report {row[0]}")
            cr = User.objects.filter(username=row[6], first_name=row[4], last_name=row[5])[0]
            ass = User.objects.filter(username=row[9], first_name=row[7], last_name=row[8])[0] if row[9] != None else None
            e = models.BuildingEntrance.objects.filter(description=row[10])[0] if row[10] != None else None
            obj = models.FaultReport(subject=row[0], description=row[1], created_by_user=cr, assigned_to_user=ass, closed=(row[3] != 0), entrance=e)
            obj.save()
            obj.created_date=row[2]
            obj.save()


            SELECT1 = '''
            SELECT r.UPLOAD_TIME, r.FILENAME, u.FIRST_NAME, u.LAST_NAME, u.LOGIN, r."DATA"
            FROM FAULT_REPORT_ATTACHMENT r
            LEFT JOIN "USER" u on u.ID = r.USER_ID
            WHERE r.FAULT_REPORT_ID = {}
            ORDER BY r.ID
            '''
            cur1 = cnn.cursor()
            cur1.execute(SELECT1.replace('{}', str(row[11])))
            for row1 in cur1:
                print(f"creating fault attachment for {row1[1]}")
                u = User.objects.filter(username=row1[4], first_name=row1[2], last_name=row1[3])[0]
                obj1 = models.FaultAsset(description='', fault_report=obj, created_by_user=u)
                data = row1[5]
                obj1.file.save(row1[1], io.BytesIO(data))
                obj1.save()
                obj1.created_date = row1[0]
                obj1.save()
            cur1.close()

            SELECT1 = '''
            SELECT u.FIRST_NAME, u.LAST_NAME, u.LOGIN, r.INSERTION_TIME, r."BODY"
            FROM FAULT_REPORT_COMMENT r
            LEFT JOIN "USER" u on u.ID = r.USER_ID
            WHERE r.FAULT_REPORT_ID = {}
            ORDER BY r.ID
            '''
            cur1 = cnn.cursor()
            cur1.execute(SELECT1.replace('{}', str(row[11])))
            for row1 in cur1:
                print(f"creating fault comment for {row1[4]}")
                u = User.objects.filter(username=row1[2], first_name=row1[0], last_name=row1[1])[0]
                obj1 = models.FaultComment(fault_report=obj, author=u, body=row1[4])
                obj1.save()
                obj1.created_date = row1[3]
                obj1.save()
            cur1.close()

            SELECT1 = '''
            SELECT u.FIRST_NAME, u.LAST_NAME, u.LOGIN
            FROM FAULT_REPORT_WATCHING r
            LEFT JOIN "USER" u on u.ID = r.USER_ID
            WHERE r.FAULT_REPORT_ID = {}
            '''
            cur1 = cnn.cursor()
            cur1.execute(SELECT1.replace('{}', str(row[11])))
            for row1 in cur1:
                print(f"creating fault watching for {row1[0]} {row1[1]}")
                u = User.objects.filter(username=row1[2], first_name=row1[0], last_name=row1[1])[0]
                obj.watching_users.add(u)
            cur1.close()
        else:
            print(f"fault report {row[0]} already exists")

    cnn.commit()


def migrate_adverts(cnn):
    SELECT = '''
    SELECT t.DESCRIPTION, r.HEADER, r.BODY, r.PHONE, r.E_MAIL, r.CREATION_DATE, r.PUBLISHED, u.FIRST_NAME, u.LAST_NAME, u.LOGIN
    FROM ADVERT r
    LEFT JOIN ADVERT_TYPE t on t.ID = r.TYPE_ID
    LEFT JOIN "USER" u on u.ID = r.USER_ID
    WHERE r.COMPANY_ID = 1
    '''
    cur = cnn.cursor()
    cur.execute(SELECT)
    for row in cur:
        i = models.Advert.objects.filter(header=row[1]).count()
        if i == 0:
            print(f"creating advert {row[1]}")
            u = User.objects.filter(username=row[9], first_name=row[7], last_name=row[8])[0]
            t = models.AdvertType.objects.filter(description=row[0])[0]
            obj = models.Advert(type=t, header=row[1], body=row[2], created_by_user=u, phone=row[3], email=row[4], published=(row[6] != 0))
            obj.save()
            obj.created_date=row[5]
            obj.save()
        else:
            print(f"advert {row[0]} already exists")
    cnn.commit()


# https://firebird-driver.readthedocs.io/en/latest/getting-started.html#installation
class Command(BaseCommand):
    help = "Migrate from fb"
    cnn = None

    def handle(self, *args, **options):
        db_login, db_password, db_database = mypwd.get_values("svjis-fb", ["login", "password", "database"])
        driver_config.stream_blob_threshold.value = 20_971_520 # 20MB
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
        migrate_article_watching(self.cnn)
        migrate_news(self.cnn)
        migrate_survey(self.cnn)
        migrate_fault_report(self.cnn)
        migrate_adverts(self.cnn)

        self.cnn.close()
        print('Done!')
