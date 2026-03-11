from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.db.models import Q
import json
from .forms import ContentForm, ContentEditForm, ContentVersionForm
from .models import Content, ContentVersion, Loader, Category, Theme
from .validators import validate_upload_size

def index(request):
    featured = Content.objects.filter(is_approved=True, is_featured=True)[:6]
    recent = Content.objects.filter(is_approved=True).order_by('-created_at')[:12]
    return render(request, 'content/index.html', {
        'featured': featured,
        'recent': recent,
    })

def browse(request):
    items = Content.objects.filter(is_approved=True)
    categories = Category.objects.all()

    category_slug = request.GET.get('category', 'mods')
    active_category = None
    if category_slug:
        try:
            active_category = Category.objects.get(slug=category_slug)
            items = items.filter(category=active_category)
        except Category.DoesNotExist:
            pass

    themes = Theme.objects.all()

    q = request.GET.get('q', '').strip()
    if q:
        items = items.filter(Q(title__icontains=q) | Q(description__icontains=q))

    theme_slug = request.GET.get('theme', '')
    if theme_slug:
        items = items.filter(theme__slug=theme_slug)

    loader_slug = request.GET.get('loader', '')
    if loader_slug:
        items = items.filter(loaders__slug=loader_slug)

    sort = request.GET.get('sort', 'downloads')
    if sort == 'downloads':
        items = items.order_by('-downloads')
    elif sort == 'title':
        items = items.order_by('title')
    else:
        items = items.order_by('-created_at')

    return render(request, 'content/browse.html', {
        'items': items,
        'categories': categories,
        'active_category': active_category,
        'themes': themes,
        'loaders': Loader.objects.all(),
        'current': {
            'q': q,
            'category': category_slug,
            'theme': theme_slug,
            'loader': loader_slug,
            'sort': sort,
        },
    })

def detail(request, slug):
    if request.user.is_authenticated:
        item = get_object_or_404(Content, slug=slug)
        if not item.is_approved and item.author != request.user:
            raise Http404
    else:
        item = get_object_or_404(Content, slug=slug, is_approved=True)

    return render(request, 'content/detail.html', {
        'item': item,
        'versions': item.versions.all(),
        'screenshots': item.screenshots.all(),
    })

@login_required
def upload(request):
    field_config = {}
    for ct in Category.objects.all():
        field_config[str(ct.id)] = {
            'loaders': ct.has_loader,
            'game_version': ct.has_game_version,
            'theme': ct.has_theme,
        }

    if request.method == 'POST':
        content_form = ContentForm(request.POST, request.FILES)
        if content_form.is_valid():
            item = content_form.save(commit=False)
            item.author = request.user
            item.save()
            content_form.save_m2m()
            messages.success(request, 'Uploaded! It will appear publicly once approved.')
            return redirect('content:detail', slug=item.slug)
    else:
        content_form = ContentForm()

    return render(request, 'content/upload.html', {
        'content_form': content_form,
        'field_config_json': json.dumps(field_config),
    })

@login_required
def edit(request, slug):
    item = get_object_or_404(Content, slug=slug, author=request.user)
    if request.method == 'POST':
        form = ContentEditForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated successfully.')
            return redirect('content:detail', slug=item.slug)
    else:
        form = ContentEditForm(instance=item)

    return render(request, 'content/edit.html', {'form': form, 'item': item, 'loaders': Loader.objects.all(), 'version_form': ContentVersionForm(),})

@login_required
def add_version(request, slug):
    item = get_object_or_404(Content, slug=slug, author=request.user)
    if request.method == 'POST':
        if not validate_upload_size(request, max_mb=500):
            messages.error(request, 'File is too large. Maximum size is 500MB.')
            return redirect(request.META.get('HTTP_REFERER', 'content:index'))
        
        form = ContentVersionForm(request.POST, request.FILES)
        if form.is_valid():
            version = form.save(commit=False)
            version.content = item
            version.file_size = version.file.size
            version.save()
            messages.success(request, f'Version {version.version_number} added.')
    return redirect(request.META.get('HTTP_REFERER', 'content:index'))

@login_required
def delete(request, slug):
    item = get_object_or_404(Content, slug=slug, author=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, f'{item.title} has been deleted.')
        return redirect('content:index')
    return redirect('content:edit', slug=slug)


def download(request, version_id):
    version = get_object_or_404(ContentVersion, pk=version_id, content__is_approved=True)
    version.content.increment_downloads()
    return redirect(version.file.url)
