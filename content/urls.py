from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    path('', views.index, name='index'),
    path('browse/', views.browse, name='browse'),
    path('upload/', views.upload, name='upload'),
    path('item/<slug:slug>/', views.detail, name='detail'),

    path('item/<slug:slug>/edit/', views.edit, name='edit'),
    path('item/<slug:slug>/addver/', views.add_version, name='add_version'),
    path('item/<slug:slug>/delete/', views.delete, name='delete'),
    path('version/<int:version_id>/delete/', views.delete_version, name='delete_version'),
    path('version/<int:version_id>/editver/', views.edit_version, name='edit_version'),

    path('download/<int:version_id>/', views.download, name='download'),
]