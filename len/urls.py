from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.LoginUser.as_view(), name='login'),

    path('export-clients-xlsx', views.get_clients_xlsx, name='clients_xlsx'),
    path('export-clients-json', views.get_clients_json, name='clients_json'),

    path('export-guests-xlsx', views.get_guests_xlsx, name='guests_xlsx'),
    path('export-guests-json', views.get_guests_json, name='guests_json'),

    path('clients/', views.ClientsList.as_view(), name='clients_list'),
    path('client/<int:pk>/', views.ClientDetail.as_view(), name='client'),
    path('client/<int:pk>/update/', views.ClientUpdate.as_view(), name='client_upd'),
    path('client/add/', views.ClientCreate.as_view(), name='client_new'),
    path('client/<int:pk>/delete/', views.ClientDelete.as_view(), name='client_delete'),

    path('client/<int:pk>/add-contact', views.ContactCreate.as_view(), name='client_new_cont'),

    # path('contact/add/', views.ContactCreate.as_view(), name='contact_new'),
    path('contact/<int:pk>/', views.ContactsDetail.as_view(), name='contact'),

    path('classes/', views.ClassesList.as_view(), name='classes_list'),
    path('class/<int:pk>/', views.ClassDetail.as_view(), name='class'),
    # path('client/<int:pk>/update/', views.ClassUpdate.as_view(), name='client_upd'),
    # path('client/add/', views.ClassCreate.as_view(), name='client_new'),
    # path('client/<int:pk>/delete/', views.ClassDelete.as_view(), name='client_delete'),
]
