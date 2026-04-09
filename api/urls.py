from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContentListView, ContentDetailView, LatestVersionView, VersionListView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

app_name = 'api'

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    path('items/', ContentListView.as_view()),

    path('item/<slug:slug>/', ContentDetailView.as_view()),
    path('item/<slug:slug>/latest/', LatestVersionView.as_view()),
    path('item/<slug:slug>/versions/', VersionListView.as_view()),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularRedocView.as_view(url_name='api:schema'), name='redoc'),
]