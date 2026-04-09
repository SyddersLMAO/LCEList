from rest_framework import serializers
from content.models import Content, Category, Loader, Theme

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']

class LoaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loader
        fields = ['name', 'slug']

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['name', 'slug']

class ContentSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    loaders = LoaderSerializer(many=True, read_only=True)
    theme = ThemeSerializer(read_only=True)
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = [
            'title', 'slug', 'tagline', 'description', 'thumbnail',
            'author', 'downloads', 'category', 'theme', 'loaders', 'tags', 'created_at'
        ]
    
    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]