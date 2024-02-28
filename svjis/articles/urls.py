from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.main_view, name='main'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('redaction/', views.redaction_view, name='redaction'),
    path('redaction_menu/', views.redaction_menu_view, name='redaction_menu'),
    path('redaction_menu_edit/<int:pk>/', views.redaction_menu_edit_view, name='redaction_menu_edit'),
    path('redaction_menu_save/', views.redaction_menu_save_view, name='redaction_menu_save'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
