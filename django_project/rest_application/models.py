from django.db import models

from .validators import valid_personal_id, valid_name, valid_age

class Profile(models.Model):
    personal_id = models.CharField(primary_key=True, max_length=50, unique=True, validators=[valid_personal_id])
    name = models.CharField(max_length=50, validators=[valid_name])
    last_name = models.CharField(max_length=50, validators=[valid_name])
    age = models.PositiveIntegerField(validators=[valid_age])

    def __str__(self):
        s = f'{self.name} {self.last_name}, ({self.personal_id})'
        return s