from django.core.exceptions import ValidationError


def valid_personal_id(value):
    value = str(value)
    value = value.replace('-', '').replace('.', '')
    if not value.isdigit():
        raise ValidationError(
            'Personal ID must be a number, not %(value)s',
            code='invalid',
            params={'value': value}
        )
    return value

def valid_name(value):
    if not value.isalpha():
        raise ValidationError(
            'Name and Last Name must be a string, not %(value)s',
            code='invalid',
            params={'value': value}
        )
    return value

def valid_age(value):
    value = str(value)
    if not value.isdigit():
        raise ValidationError(
            'Age must be a number, not %(value)s',
            code='invalid',
            params={'value': value}
        )
    return value