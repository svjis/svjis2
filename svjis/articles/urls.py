from . import views, views_contact, views_personal_settings, views_redaction, views_faults, views_adverts, views_admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.main_view, name='main'),
    path('main/<int:menu>', views.main_filtered_view, name='main_filtered'),
    path('article_survey_vote/', views.article_survey_vote_view, name='article_survey_vote'),
    path('article/<str:slug>/', views.article_view, name='article'),
    path('article_comment_save/', views.article_comment_save_view, name='article_comment_save'),
    path('article_watch/', views.article_watch_view, name='article_watch'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('contact_company/', views_contact.contact_view, name='contact_company'),
    path('contact_phonelist/', views_contact.phonelist_view, name='contact_phonelist'),
    path(
        'personal_settings_edit/', views_personal_settings.personal_settings_edit_view, name='personal_settings_edit'
    ),
    path(
        'personal_settings_save/', views_personal_settings.personal_settings_save_view, name='personal_settings_save'
    ),
    path('personal_my_units/', views_personal_settings.personal_my_units_view, name='personal_my_units'),
    path(
        'personal_settings_password/',
        views_personal_settings.personal_settings_password_view,
        name='personal_settings_password',
    ),
    path(
        'personal_settings_password_save/',
        views_personal_settings.personal_settings_password_save_view,
        name='personal_settings_password_save',
    ),
    path('redaction_menu/', views_redaction.redaction_menu_view, name='redaction_menu'),
    path('redaction_menu_edit/<int:pk>/', views_redaction.redaction_menu_edit_view, name='redaction_menu_edit'),
    path('redaction_menu_save/', views_redaction.redaction_menu_save_view, name='redaction_menu_save'),
    path('redaction_menu_delete/<int:pk>/', views_redaction.redaction_menu_delete_view, name='redaction_menu_delete'),
    path('redaction_article/', views_redaction.redaction_article_view, name='redaction_article'),
    path(
        'redaction_article_edit/<int:pk>/', views_redaction.redaction_article_edit_view, name='redaction_article_edit'
    ),
    path('redaction_article_save/', views_redaction.redaction_article_save_view, name='redaction_article_save'),
    path(
        'redaction_article_notifications/<int:pk>/',
        views_redaction.redaction_article_notifications_view,
        name='redaction_article_notifications',
    ),
    path(
        'redaction_article_notifications_send',
        views_redaction.redaction_article_notifications_send_view,
        name='redaction_article_notifications_send',
    ),
    path(
        'redaction_article_asset_save/',
        views_redaction.redaction_article_asset_save_view,
        name='redaction_article_asset_save',
    ),
    path(
        'redaction_article_asset_delete/<int:pk>/',
        views_redaction.redaction_article_asset_delete_view,
        name='redaction_article_asset_delete',
    ),
    path('redaction_news/', views_redaction.redaction_news_view, name='redaction_news'),
    path('redaction_news_edit/<int:pk>/', views_redaction.redaction_news_edit_view, name='redaction_news_edit'),
    path('redaction_news_save/', views_redaction.redaction_news_save_view, name='redaction_news_save'),
    path('redaction_news_delete/<int:pk>/', views_redaction.redaction_news_delete_view, name='redaction_news_delete'),
    path('redaction_useful_link/', views_redaction.redaction_useful_link_view, name='redaction_useful_link'),
    path(
        'redaction_useful_link_edit/<int:pk>/',
        views_redaction.redaction_useful_link_edit_view,
        name='redaction_useful_link_edit',
    ),
    path(
        'redaction_useful_link_save/',
        views_redaction.redaction_useful_link_save_view,
        name='redaction_useful_link_save',
    ),
    path(
        'redaction_useful_link_delete/<int:pk>/',
        views_redaction.redaction_useful_link_delete_view,
        name='redaction_useful_link_delete',
    ),
    path('redaction_survey/', views_redaction.redaction_survey_view, name='redaction_survey'),
    path('redaction_survey_edit/<int:pk>/', views_redaction.redaction_survey_edit_view, name='redaction_survey_edit'),
    path('redaction_survey_save/', views_redaction.redaction_survey_save_view, name='redaction_survey_save'),
    path(
        'redaction_survey_delete/<int:pk>/',
        views_redaction.redaction_survey_delete_view,
        name='redaction_survey_delete',
    ),
    path(
        'redaction_survey_option_delete/<int:pk>/',
        views_redaction.redaction_survey_option_delete_view,
        name='redaction_survey_option_delete',
    ),
    path(
        'redaction_survey_results/<int:pk>/',
        views_redaction.redaction_survey_results_view,
        name='redaction_survey_results',
    ),
    path(
        'redaction_survey_results_export_to_excel/<int:pk>/',
        views_redaction.redaction_survey_results_export_to_excel_view,
        name='redaction_survey_results_export_to_excel',
    ),
    path('fault/<str:slug>/', views_faults.fault_view, name='fault'),
    path('faults_list/', views_faults.faults_list_view, name='faults_list'),
    path('faults_fault_create/', views_faults.faults_fault_create_view, name='faults_fault_create'),
    path('faults_fault_edit/<int:pk>/', views_faults.faults_fault_edit_view, name='faults_fault_edit'),
    path(
        'faults_fault_take_ticket/<int:pk>/',
        views_faults.faults_fault_take_ticket_view,
        name='faults_fault_take_ticket',
    ),
    path(
        'faults_fault_close_ticket/<int:pk>/',
        views_faults.faults_fault_close_ticket_view,
        name='faults_fault_close_ticket',
    ),
    path('faults_fault_create_save/', views_faults.faults_fault_create_save_view, name='faults_fault_create_save'),
    path('faults_fault_update/', views_faults.faults_fault_update_view, name='faults_fault_update'),
    path('faults_fault_asset_save/', views_faults.faults_fault_asset_save_view, name='faults_fault_asset_save'),
    path(
        'faults_fault_asset_delete/<int:pk>/',
        views_faults.faults_fault_asset_delete_view,
        name='faults_fault_asset_delete',
    ),
    path('fault_comment_save/', views_faults.fault_comment_save_view, name='fault_comment_save'),
    path('fault_watch/', views_faults.fault_watch_view, name='fault_watch'),
    path('adverts_list/', views_adverts.adverts_list_view, name='adverts_list'),
    path('adverts_edit/<int:pk>/', views_adverts.adverts_edit_view, name='adverts_edit'),
    path('adverts_save/', views_adverts.adverts_save_view, name='adverts_save'),
    path('adverts_asset_save/', views_adverts.adverts_asset_save_view, name='adverts_asset_save'),
    path('adverts_asset_delete/<int:pk>/', views_adverts.adverts_asset_delete_view, name='adverts_asset_delete'),
    path('admin_company_edit/', views_admin.admin_company_edit_view, name='admin_company_edit'),
    path('admin_company_save/', views_admin.admin_company_save_view, name='admin_company_save'),
    path('admin_board/', views_admin.admin_board_view, name='admin_board'),
    path('admin_board_edit/<int:pk>/', views_admin.admin_board_edit_view, name='admin_board_edit'),
    path('admin_board_save/', views_admin.admin_board_save_view, name='admin_board_save'),
    path('admin_board_delete/<int:pk>/', views_admin.admin_board_delete_view, name='admin_board_delete'),
    path('admin_building_edit/', views_admin.admin_building_edit_view, name='admin_building_edit'),
    path('admin_building_save/', views_admin.admin_building_save_view, name='admin_building_save'),
    path('admin_entrance/', views_admin.admin_entrance_view, name='admin_entrance'),
    path('admin_entrance_edit/<int:pk>/', views_admin.admin_entrance_edit_view, name='admin_entrance_edit'),
    path('admin_entrance_save/', views_admin.admin_entrance_save_view, name='admin_entrance_save'),
    path('admin_entrance_delete/<int:pk>/', views_admin.admin_entrance_delete_view, name='admin_entrance_delete'),
    path('admin_building_unit/', views_admin.admin_building_unit_view, name='admin_building_unit'),
    path(
        'admin_building_unit_edit/<int:pk>/',
        views_admin.admin_building_unit_edit_view,
        name='admin_building_unit_edit',
    ),
    path('admin_building_unit_save/', views_admin.admin_building_unit_save_view, name='admin_building_unit_save'),
    path(
        'admin_building_unit_delete/<int:pk>/',
        views_admin.admin_building_unit_delete_view,
        name='admin_building_unit_delete',
    ),
    path(
        'admin_building_unit_owners/<int:pk>/',
        views_admin.admin_building_unit_owners_view,
        name='admin_building_unit_owners',
    ),
    path(
        'admin_building_unit_owners_save',
        views_admin.admin_building_unit_owners_save_view,
        name='admin_building_unit_owners_save',
    ),
    path(
        'admin_building_unit_owners_delete/<int:pk>/<int:owner>/',
        views_admin.admin_building_unit_owners_delete_view,
        name='admin_building_unit_owners_delete',
    ),
    path(
        'admin_building_unit_export_to_excel/',
        views_admin.admin_building_unit_export_to_excel_view,
        name='admin_building_unit_export_to_excel',
    ),
    path('admin_user/', views_admin.admin_user_view, name='admin_user'),
    path('admin_user_edit/<int:pk>/', views_admin.admin_user_edit_view, name='admin_user_edit'),
    path('admin_user_save/', views_admin.admin_user_save_view, name='admin_user_save'),
    path('admin_user_owns/<int:pk>/', views_admin.admin_user_owns_view, name='admin_user_owns'),
    path('admin_user_owns_save', views_admin.admin_user_owns_save_view, name='admin_user_owns_save'),
    path(
        'admin_user_owns_delete/<int:pk>/<int:owner>/',
        views_admin.admin_user_owns_delete_view,
        name='admin_user_owns_delete',
    ),
    path(
        'admin_user_export_to_excel/', views_admin.admin_user_export_to_excel_view, name='admin_user_export_to_excel'
    ),
    path('admin_group/', views_admin.admin_group_view, name='admin_group'),
    path('admin_group_edit/<int:pk>/', views_admin.admin_group_edit_view, name='admin_group_edit'),
    path('admin_group_save/', views_admin.admin_group_save_view, name='admin_group_save'),
    path('admin_group_delete/<int:pk>/', views_admin.admin_group_delete_view, name='admin_group_delete'),
    path('admin_preferences/', views_admin.admin_preferences_view, name='admin_preferences'),
    path('admin_preferences_edit/<int:pk>/', views_admin.admin_preferences_edit_view, name='admin_preferences_edit'),
    path('admin_preferences_save/', views_admin.admin_preferences_save_view, name='admin_preferences_save'),
    path(
        'admin_preferences_delete/<int:pk>/',
        views_admin.admin_preferences_delete_view,
        name='admin_preferences_delete',
    ),
    path('admin_messages/', views_admin.admin_messages_view, name='admin_messages'),
    path('lost_password/', views_personal_settings.lost_password_view, name='lost_password'),
    path('lost_password_send/', views_personal_settings.lost_password_send_view, name='lost_password_send'),
    path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
