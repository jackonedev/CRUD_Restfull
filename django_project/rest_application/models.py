from django.db import models
from django.core.exceptions import ValidationError


def valid_personal_id(value):
    value = str(value)
    value = value.replace('-', '').replace('.', '')
    if not value.isdigit():
        raise ValidationError(f'Personal ID must be a number, not {value}')
    return value

def valid_name(value):
    if not value.isalpha():
        raise ValidationError(f'Name must be a string, not {value}')
    return value

def valid_age(value):
    value = str(value)
    if not value.isdigit():
        raise ValidationError(f'Age must be a number, not {value}')
    return value

class Profile(models.Model):
    personal_id = models.CharField(primary_key=True, max_length=50, unique=True, validators=[valid_personal_id])
    name = models.CharField(max_length=50, validators=[valid_name])
    last_name = models.CharField(max_length=50, validators=[valid_name])
    age = models.PositiveIntegerField(validators=[valid_age])

    def __str__(self):
        s = f'{self.name} {self.last_name}, ({self.personal_id})'
        return s