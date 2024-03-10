from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group, Permission
from articles.models import ArticleMenu, Preferences


def create_groups():
    names = [
            {'name': 'Administrator', 'perms': [
                        'svjis_view_redaction_menu',
                        'svjis_edit_article',
                        'svjis_add_article_comment',
                        'svjis_edit_article_menu',
                        'svjis_edit_article_news',
                        'svjis_view_admin_menu',
                        'svjis_edit_admin_users',
                        'svjis_edit_admin_groups',
                        'svjis_view_personal_menu',
                        'svjis_edit_admin_preferences',
                        'svjis_edit_admin_company',
                        'svjis_edit_admin_building',
        ]},
            {'name': 'Vlastník', 'perms': [
                        'svjis_add_article_comment',
                        'svjis_view_personal_menu',
        ]},
            {'name': 'Člen výboru', 'perms': [
                        'svjis_view_redaction_menu',
                        'svjis_edit_article',
                        'svjis_add_article_comment',
                        'svjis_edit_article_menu',
                        'svjis_edit_article_news',
                        'svjis_view_personal_menu',
        ]},
            {'name': 'Dodavatel', 'perms': [
                        'svjis_add_article_comment',
                        'svjis_view_personal_menu',
        ]},
            {'name': 'Redaktor', 'perms': [
                        'svjis_view_redaction_menu',
                        'svjis_edit_article',
                        'svjis_add_article_comment',
                        'svjis_edit_article_news',
                        'svjis_view_personal_menu',
        ]},
    ]

    print("Creating groups...")
    for g in names:
        gobj = Group(name=g['name'])
        gobj.save()
        for p in g['perms']:
            try:
                pobj = Permission.objects.get(content_type__app_label='articles', codename=p)
                gobj.permissions.add(pobj)
            except:
                print(f"Permission {p} doesnt exist")
    print("Done")


def create_admin_user():
    print("Creating admin user...")
    u = User.objects.create(username='admin',
                            email='admin@test.cz',
                            password=make_password('masterkey'),
                            last_name='admin')
    u.is_active = True
    u.is_staff = True
    u.is_superuser = True
    u.save()
    g = Group.objects.get(name='Administrator')
    u.groups.add(g)
    print("Done")


def create_article_menu():
    print("Creating article menu...")
    menu = ['Vývěska', 'Dotazy a návody' ,'Smlouvy' ,'Zápisy']
    for m in menu:
        ArticleMenu.objects.create(description=m)
    print("Done")


def create_preferences():
    print("Creating preferences...")
    preferences = [
        {
            'key': 'mail.template.lost.password',
            'value': '<html><body>Dobrý den,<br>Vaše přihlašovací údaje jsou:<br><br>{}<br>Heslo si můžete změnit v menu <b>Osobní nastavení - Změna hesla</b><br><br>Web SVJ</body></html>'
        },
    ]
    for p in preferences:
        Preferences.objects.create(key=p['key'], value=p['value'])
    print("Done")


class Command(BaseCommand):
    help = "Populate database with initial data"

    def handle(self, *args, **options):
        create_article_menu()
        create_groups()
        create_preferences()
        create_admin_user()
