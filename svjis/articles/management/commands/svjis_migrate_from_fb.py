from django.core.management.base import BaseCommand
import mypwd
from firebird.driver import connect
from django.contrib.auth.models import Group


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

        migrate_groups(self.cnn)
        self.cnn.close()
