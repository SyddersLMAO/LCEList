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

    path('download/<int:version_id>/', views.download, name='download'),
]