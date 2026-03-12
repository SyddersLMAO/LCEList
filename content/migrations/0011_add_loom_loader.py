from django.db import migrations

def add_loom_loader(apps, schema_editor):
    Loader = apps.get_model('content', 'Loader')
    Loader.objects.get_or_create(name='Loom', slug='loom')

def remove_loom_loader(apps, schema_editor):
    Loader = apps.get_model('content', 'Loader')
    Loader.objects.filter(name='Loom').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('content', '0010_alter_content_thumbnail_alter_contentversion_file'),
    ]

    operations = [
        migrations.RunPython(add_loom_loader, remove_loom_loader),
    ]
