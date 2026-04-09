from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as django_filters
from django.shortcuts import get_object_or_404
from content.models import Content
from .serializers import ContentSerializer

class ContentFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug')
    theme = django_filters.CharFilter(field_name='theme__slug')
    loader = django_filters.CharFilter(field_name='loaders__slug')

    class Meta:
        model = Content
        fields = ['category', 'theme', 'loader']

class ContentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Content.objects.filter(is_approved=True)
    serializer_class = ContentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ContentFilter

    search_fields = ['title', 'description']

    ordering_fields = ['downloads', 'created_at']
    ordering = ['-downloads']

class ContentDetailView(RetrieveAPIView):
    queryset = Content.objects.filter(is_approved=True)
    serializer_class = ContentSerializer
    lookup_field = 'slug'

class LatestVersionView(APIView):
    def get(self, request, slug):
        content = get_object_or_404(Content, slug=slug, is_approved=True)

        versions = content.versions.all()

        loader = request.query_params.get('loader')
        game_version = request.query_params.get('game_version')

        if loader:
            versions = versions.filter(loader__slug=loader)

        if game_version:
            versions = versions.filter(game_version=game_version)

        version = versions.first()

        if not version:
            return Response({"error": "No matching version found"}, status=404)

        return Response({
            "content": content.slug,
            "version": version.version_number,
            "game_version": version.game_version,
            "loader": version.loader.slug if version.loader else None,
            "download_url": request.build_absolute_uri(version.file.url),
            "file_size": version.file_size,
            "created_at": version.created_at,
        })

class VersionListView(APIView):
    def get(self, request, slug):
        content = get_object_or_404(Content, slug=slug, is_approved=True)

        versions = content.versions.all()

        loader = request.query_params.get('loader')
        game_version = request.query_params.get('game_version')

        if loader:
            versions = versions.filter(loader__slug=loader)

        if game_version:
            versions = versions.filter(game_version=game_version)

        data = []

        for v in versions:
            data.append({
                "version": v.version_number,
                "game_version": v.game_version,
                "loader": v.loader.slug if v.loader else None,
                "download_url": request.build_absolute_uri(v.file.url),
                "file_size": v.file_size,
                "created_at": v.created_at,
            })

        return Response(data)