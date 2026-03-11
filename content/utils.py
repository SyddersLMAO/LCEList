from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

def crop_to_square(image_field):
    """Crops an ImageField to a 1:1 square from the center."""
    img = Image.open(image_field)
    
    if img.mode not in ('RGB', 'RGBA'):
        img = img.convert('RGB')

    width, height = img.size
    size = min(width, height)

    left = (width - size) // 2
    top = (height - size) // 2
    right = left + size
    bottom = top + size

    img = img.crop((left, top, right, bottom))

    output = BytesIO()
    img.save(output, format='PNG', quality=90)
    output.seek(0)

    return ContentFile(output.read(), name=image_field.name.split('/')[-1])