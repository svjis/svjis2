from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Article


class StaticViewSitemap(Sitemap):
    def items(self):
        return ['main', 'contact']

    def location(self, item):
        return reverse(item)

    def changefreq(self, item):
        return {'main': 'daily', 'contact': 'monthly'}[item]


class ArticleSitemap(Sitemap):
    def items(self):
        return Article.objects.filter(published=True, visible_for_all=True).order_by('created_date')

    def lastmod(self, obj):
        return obj.created_date
