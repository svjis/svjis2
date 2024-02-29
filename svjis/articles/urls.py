from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.main_view, name='main'),
    path('main/<int:menu>', views.main_filtered_view, name='main_filtered'),
    path('article/<int:pk>/', views.article_view, name='article'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('redaction_menu/', views.redaction_menu_view, name='redaction_menu'),
    path('redaction_menu_edit/<int:pk>/', views.redaction_menu_edit_view, name='redaction_menu_edit'),
    path('redaction_menu_save/', views.redaction_menu_save_view, name='redaction_menu_save'),
    path('redaction_menu_delete/<int:pk>/', views.redaction_menu_delete_view, name='redaction_menu_delete'),
    path('redaction_article/', views.redaction_article_view, name='redaction_article'),
    path('redaction_article_edit/<int:pk>/', views.redaction_article_edit_view, name='redaction_article_edit'),
    path('redaction_article_save/', views.redaction_article_save_view, name='redaction_article_save'),
    path('redaction_article_delete/<int:pk>/', views.redaction_article_delete_view, name='redaction_article_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
