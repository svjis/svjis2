from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Article)
admin.site.register(models.ArticleLog)
admin.site.register(models.ArticleAsset)
admin.site.register(models.ArticleComment)
admin.site.register(models.ArticleMenu)
admin.site.register(models.News)
admin.site.register(models.UsefulLink)
admin.site.register(models.Survey)
admin.site.register(models.SurveyOption)
admin.site.register(models.SurveyAnswerLog)
admin.site.register(models.UserProfile)
admin.site.register(models.MessageQueue)
admin.site.register(models.Preferences)
admin.site.register(models.Company)
admin.site.register(models.Building)
admin.site.register(models.Board)
admin.site.register(models.BuildingEntrance)
admin.site.register(models.BuildingUnitType)
admin.site.register(models.BuildingUnit)
admin.site.register(models.FaultReport)
admin.site.register(models.FaultAsset)
admin.site.register(models.FaultComment)
admin.site.register(models.AdvertType)
admin.site.register(models.Advert)
admin.site.register(models.AdvertAsset)
