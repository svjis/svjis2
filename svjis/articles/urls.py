from . import views
from . import views_redaction
from . import views_admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.main_view, name='main'),
    path('main/<int:menu>', views.main_filtered_view, name='main_filtered'),
    path('article/<int:pk>/', views.article_view, name='article'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('redaction_menu/', views_redaction.redaction_menu_view, name='redaction_menu'),
    path('redaction_menu_edit/<int:pk>/', views_redaction.redaction_menu_edit_view, name='redaction_menu_edit'),
    path('redaction_menu_save/', views_redaction.redaction_menu_save_view, name='redaction_menu_save'),
    path('redaction_menu_delete/<int:pk>/', views_redaction.redaction_menu_delete_view, name='redaction_menu_delete'),
    path('redaction_article/', views_redaction.redaction_article_view, name='redaction_article'),
    path('redaction_article_edit/<int:pk>/', views_redaction.redaction_article_edit_view, name='redaction_article_edit'),
    path('redaction_article_save/', views_redaction.redaction_article_save_view, name='redaction_article_save'),
    path('redaction_article_delete/<int:pk>/', views_redaction.redaction_article_delete_view, name='redaction_article_delete'),
    path('redaction_article_asset_save/', views_redaction.redaction_article_asset_save_view, name='redaction_article_asset_save'),
    path('redaction_article_asset_delete//<int:pk>/', views_redaction.redaction_article_asset_delete_view, name='redaction_article_asset_delete'),
    path('redaction_news/', views_redaction.redaction_news_view, name='redaction_news'),
    path('redaction_news_edit/<int:pk>/', views_redaction.redaction_news_edit_view, name='redaction_news_edit'),
    path('redaction_news_save/', views_redaction.redaction_news_save_view, name='redaction_news_save'),
    path('redaction_news_delete/<int:pk>/', views_redaction.redaction_news_delete_view, name='redaction_news_delete'),
    path('admin_user/', views_admin.admin_user_view, name='admin_user'),
    path('admin_user_edit/<int:pk>/', views_admin.admin_user_edit_view, name='admin_user_edit'),
    path('admin_user_save/', views_admin.admin_user_save_view, name='admin_user_save'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
