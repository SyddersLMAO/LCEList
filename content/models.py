from django.db import models
from django.conf import settings
from django.utils.text import slugify
from taggit.managers import TaggableManager
from .validators import validate_image_size, validate_content_file_size, validate_zip_file
from .utils import crop_to_square

class Loader(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    has_loader = models.BooleanField(default=False)
    has_game_version = models.BooleanField(default=False)
    has_theme = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

class Theme(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']


class Content(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    tagline = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True, default='images/item_icon.png', validators=[validate_image_size])
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name='content',
    )
    downloads = models.PositiveIntegerField(default=0)

    loaders = models.ManyToManyField(Loader, related_name='content', blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='content',
    )
    theme = models.ForeignKey(
        Theme,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='content',
    )
    game_version = models.CharField(max_length=50, blank=True)
    tags = TaggableManager(blank=True)

    issues_link = models.CharField(blank=True)
    source_link = models.CharField(blank=True)
    wiki_link = models.CharField(blank=True)
    discord_link = models.CharField(blank=True)
    
    is_approved = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.thumbnail and hasattr(self.thumbnail, 'file'):
            self.thumbnail = crop_to_square(self.thumbnail)
        super().save(*args, **kwargs)

    def increment_downloads(self):
        Content.objects.filter(pk=self.pk).update(
            downloads=models.F('downloads') + 1
        )
    
    @property
    def version_loaders(self):
        return set(v.loader for v in self.versions.all() if v.loader)

    class Meta:
        ordering = ['-created_at']


def version_file_path(instance, filename):
    return f'content/{instance.content.slug}/{instance.version_number}/{filename}'


class ContentVersion(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='versions')
    version_number = models.CharField(max_length=50)
    file = models.FileField(upload_to=version_file_path, validators=[validate_content_file_size, validate_zip_file])
    file_size = models.PositiveBigIntegerField(default=0)
    changelog = models.TextField(blank=True)
    game_version = models.CharField(max_length=50, blank=True)
    loader = models.ForeignKey(Loader, on_delete=models.SET_NULL, null=True, blank=True, related_name='versions')
    loader_version = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.content.title} - v{self.version_number}'

    def file_size_mb(self):
        return round(self.file_size / (1024 * 1024), 2)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('content', 'version_number')


class Screenshot(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='screenshots')
    image = models.ImageField(upload_to='screenshots/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']