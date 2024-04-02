from django.core.files import File
from django.core.management.base import BaseCommand
import base64
from articles import models


class Command(BaseCommand):
    help = "Upload test"

    def handle(self, *args, **options):
        FILE = 'C:/Users/jarberan/Desktop/Screens/euser01.png'
        with open(FILE, "rb") as image_file:
            a = models.Article.objects.filter(header='Klimatizace podmínky')[0]
            obj = models.ArticleAsset(description='', article=a)
            obj.file.save('euser01.png', image_file)
            obj.save()
