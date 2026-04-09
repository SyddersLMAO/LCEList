from django import forms
from .models import Content, ContentVersion, Category

input_classes = "w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-sm text-gray-100 focus:outline-none focus:border-pink-300"


class ContentForm(forms.ModelForm):
    slug = forms.SlugField(
        label='URL',
        help_text='lcelist.xyz/item/',
    )

    class Meta:
        model = Content
        fields = ['category', 'title', 'slug', 'tagline']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter name'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs['class'] = input_classes


class ContentEditForm(forms.ModelForm):
    slug = forms.SlugField(
        label='URL',
        help_text='lcelist.xyz/item/',
    )

    class Meta:
        model = Content
        fields = ['category', 'title', 'slug', 'tagline', 'description', 'thumbnail', 'loaders', 'theme', 'tags', 'issues_link', 'source_link', 'wiki_link', 'discord_link']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter name'}),
            'description': forms.Textarea(attrs={'rows': 20}),
            'loaders': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        category = None
        if self.instance and self.instance.category_id:
            category = self.instance.category
        elif 'category' in self.data:
            try:
                category = Category.objects.get(pl=self.data['category'])
            except Category.DoesNotExist:
                pass

        if category:
            if not category.has_loader:
                self.fields.pop('loaders', None)
            if not category.has_theme:
                self.fields.pop('theme', None)

        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs['class'] = input_classes


class ContentVersionForm(forms.ModelForm):
    class Meta:
        model = ContentVersion
        fields = ['version_number', 'file', 'loader', 'loader_version', 'changelog']
        widgets = {
            'version_number': forms.TextInput(attrs={'placeholder': 'e.g. 1.0'}),
            'loader_version': forms.TextInput(attrs={'placeholder': 'e.g. 0.15.0'}),
            'changelog': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, content=None, **kwargs):
        super().__init__(*args, **kwargs)

        category = content.category if content else None
        if category:
            if not category.has_loader:
                self.fields.pop('loader', None)
                self.fields.pop('loader_version', None)

        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs['class'] = input_classes