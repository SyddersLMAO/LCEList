from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListAPIView
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

@extend_schema(
    summary="List items",
    description="List items uploaded to the site. Supports filtering with category, theme, and loader.",
    parameters=[
        OpenApiParameter(
            name='category',
            description='Which category to use when searching (e.g. mods, worlds, etc)',
            required=False,
            type=str
        ),
        OpenApiParameter(
            name='loader',
            description='Which loader to use when searching (e.g. axo)',
            required=False,
            type=str
        ),
        OpenApiParameter(
            name='theme',
            description='Which theme to use when searching (e.g. magic, utility, etc)',
            required=False,
            type=str
        ),
    ]
)
class ContentListView(ListAPIView):
    queryset = Content.objects.filter(is_approved=True)
    serializer_class = ContentSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ContentFilter

    search_fields = ['title', 'description']
    ordering_fields = ['downloads', 'created_at']
    ordering = ['-downloads']

@extend_schema(
    summary="Retrieve item",
    description="Retrieves information about the item you have selected.",
)
class ContentDetailView(RetrieveAPIView):
    queryset = Content.objects.filter(is_approved=True)
    serializer_class = ContentSerializer
    lookup_field = 'slug'

@extend_schema(
    summary="Get latest version",
    description="Returns the latest version. You are able to filter by loader.",
    parameters=[
        OpenApiParameter(
            name='loader',
            description='Filter by loader (e.g. axo)',
            required=False,
            type=str
        ),
    ]
)
class LatestVersionView(APIView):
    def get(self, request, slug):
        content = get_object_or_404(Content, slug=slug, is_approved=True)

        versions = content.versions.all()

        loader = request.query_params.get('loader')

        if loader:
            versions = versions.filter(loader__slug=loader)

        version = versions.first()

        if not version:
            return Response({"error": "No matching version found"}, status=404)

        return Response({
            "content": content.slug,
            "version": version.version_number,
            "loader": version.loader.slug if version.loader else None,
            "download_url": request.build_absolute_uri(version.file.url),
            "file_size": version.file_size,
            "created_at": version.created_at,
        })

@extend_schema(
    summary="Get all versions",
    description="Returns all versions download link. You are able to filter by loader.",
    parameters=[
        OpenApiParameter(
            name='loader',
            description='Filter by loader (e.g. axo)',
            required=False,
            type=str
        ),
    ]
)
class VersionListView(APIView):
    def get(self, request, slug):
        content = get_object_or_404(Content, slug=slug, is_approved=True)

        versions = content.versions.all()

        loader = request.query_params.get('loader')

        if loader:
            versions = versions.filter(loader__slug=loader)

        data = []

        for v in versions:
            data.append({
                "version": v.version_number,
                "loader": v.loader.slug if v.loader else None,
                "download_url": request.build_absolute_uri(v.file.url),
                "file_size": v.file_size,
                "created_at": v.created_at,
            })

        return Response(data)