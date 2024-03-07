from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group, Permission
from articles.models import ArticleMenu


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
        ]},
            {'name': 'Vlastník', 'perms': [
                        'svjis_add_article_comment',
        ]},
            {'name': 'Člen výboru', 'perms': [
                        'svjis_view_redaction_menu',
                        'svjis_edit_article',
                        'svjis_add_article_comment',
                        'svjis_edit_article_menu',
                        'svjis_edit_article_news',
        ]},
            {'name': 'Dodavatel', 'perms': [
                        'svjis_add_article_comment',
        ]},
            {'name': 'Redaktor', 'perms': [
                        'svjis_view_redaction_menu',
                        'svjis_edit_article',
                        'svjis_add_article_comment',
                        'svjis_edit_article_news',
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


def create_admin():
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


class Command(BaseCommand):
    help = "Populate database with initial data"

    def handle(self, *args, **options):
        create_article_menu()
        create_groups()
        create_admin()
