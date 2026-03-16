from django.core.exceptions import ValidationError
from PIL import Image

def validate_file_size(max_mb):
    def validator(file):
        if file.size > max_mb * 1024 * 1024:
            raise ValidationError(f'File size must be under {max_mb}MB. Yours is {round(file.size / 1024 / 1024, 1)}MB.')
    return validator

def validate_upload_size(request, max_mb):
    content_length = request.META.get('CONTENT_LENGTH', 0)
    try:
        if int(content_length) > max_mb * 1024 * 1024:
            return False
    except (ValueError, TypeError):
        pass
    return True

def validate_zip_file(file):
    if not file.name.endswith('.zip'):
        raise ValidationError('Only .zip files are allowed.')
    
def validate_image_type(file):
    try:
        img = Image.open(file)
        if img.format not in ['JPEG', 'PNG', 'GIF', 'WEBP']:
            raise ValidationError('Unsupported image type. Please upload a JPEG, PNG, GIF or WebP.')
    except ValidationError:
        raise
    except Exception:
        raise ValidationError('Invalid image file.')
    finally:
        file.seek(0)

def validate_image_size(file):
    validate_file_size(5)(file)

def validate_content_file_size(file):
    validate_file_size(500)(file)