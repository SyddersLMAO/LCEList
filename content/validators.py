from django.core.exceptions import ValidationError

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

def validate_image_size(file):
    validate_file_size(5)(file)

def validate_content_file_size(file):
    validate_file_size(500)(file)