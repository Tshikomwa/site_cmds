from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('booking/', views.booking, name='booking'),
    path('service/', views.service, name='service'),
    path('contact/', views.contact, name='contact'),
    path('team/', views.team, name='team'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('comptabilité/resume/', views.summary_view, name='comptabilité/resume'),
    ##################################################################################
    path('gestion/', views.gestion, name='gestion'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('user_list/', views.user_list_view, name='user_list'),
    path('users/delete/<int:user_id>/', views.delete_user_view, name='delete_user'),  # Assurez-vous que ce chemin est bien défini
    path('logout/', views.custom_logout, name='logout'),
    ##################################################################################
    path('acces/', views.acces_view, name='acces'),
    ##################################################################################
    path('ress_hum/', views.ress_hum_view, name='ress_hum'),
    path('ges_adm/', views.ges_adm_view, name='ges_adm'),
    path('ges_fin/', views.ges_fin_view, name='ges_fin'),
    ##################################################################################
    path('files/upload_file/', views.upload_file, name='files/upload_file'),
    path('files/file_list/', views.file_list_view, name='files/file_list'),
    path('delete_file/<int:file_id>/', views.delete_file_view, name='delete_file'),
    ##################################################################################
    ##################################################################################
    path('service/plus1/', views.plus1, name='service/plus1'),
    path('service/plus2/', views.plus2, name='service/plus2'),
    path('service/plus3/', views.plus3, name='service/plus3'),
    path('service/plus4/', views.plus4, name='service/plus4'),
    path('service/plus5/', views.plus5, name='service/plus5'),
    path('service/plus6/', views.plus6, name='service/plus6'),
    ##################################################################################
    ##################################################################################
    path('comptabilité/r_flux/', views.r_flux, name='comptabilité/r_flux'),
    path('comptabilité/r_flux/<str:date>/', views.r_flux_detail, name='comptabilité/r_flux_detail'),
    path('form/supprimer/<int:pk>/', views.delete_r_flux, name='comptabilité/r_flux_delete'),
    path('form/<int:form_id>/pdf/', views.generate_pdf_document, name='generate_pdf_document'),
    ##################################################################################
    ##################################################################################
    ##################################################################################
    ##################################################################################
    path('comptabilité/r_vente/', views.r_vente, name='comptabilité/r_vente'),
    path('comptabilité/r_vente/<str:date>/', views.r_vente_detail, name='comptabilité/r_vente_detail'),
    path('comptabilité/r_vente/supprimer/<int:pk>/', views.delete_r_vente, name='comptabilité/r_vente_delete'),  # 🔥 Vérifie bien cette ligne !
    path('form/<int:form_id>/pdf/', views.generate_pdf_document, name='generate_pdf_document'),
    ##################################################################################
    ##################################################################################
    path('comptabilité/declaration/', views.declaration, name='comptabilité/declaration'),
    path('comptabilité/declaration/<int:pk>/', views.declaration_detail, name='declaration_detail'),
    path('comptabilité/declaration/delete/<int:pk>/', views.delete_declaration, name='delete_declaration'),
    path('form/<int:form_id>/pdf/', views.generate_pdf_coûtdocument, name='generate_pdf_coûtdocument'),
    ##################################################################################
    ##################################################################################
    path('comptabilité/', views.liste, name='comptabilité/liste'),
    path('comptabilité/ajouter/', views.ajouter, name='comptabilité/ajouter'),
    path('decaissements/modifier/<int:pk>/', views.modifier, name='comptabilité/modifier'),
    path('decaissements/supprimer/<int:pk>/', views.supprimer_dec, name='comptabilité/supprimer_dec'),
    path('decaissements/rechercher/', views.rechercher_decaissements, name='comptabilité/rechercher'),
    path('decaissements/<int:pk>/', views.detail_decaissement, name='comptabilité/detail'),
    path('comptabilité/filtrer/', views.filter_decaissements, name='comptabilité/filtrer'),
    path('comptabilité/resultats_filtre', views.resultats_filtre, name='comptabilité/resultats_filtre'),
    path('comptabilité/generate_pdf_décaissement/', views.generate_pdf_décaissement, name='comptabilité/generate_pdf_décaissement'),
    ##################################################################################
    ##################################################################################
    path('form/<int:form_id>/pdf/', views.generate_pdf_document, name='generate_pdf_document'),
    ##################################################################################  
    path("main/contact/", views.contact, name="main/contact"),
    path('messages/', views.list_messages, name='list_messages'),
    path('messages/<int:message_id>/', views.message_detail, name='message_detail'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

