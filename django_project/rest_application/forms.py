from django import forms

from .models import Profile

from .validators import valid_personal_id, valid_name, valid_age


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['personal_id', 'name', 'last_name', 'age']

    def clean_personal_id(self):
        personal_id = self.cleaned_data['personal_id']
        return valid_personal_id(personal_id)

    def clean_name(self):
        name = self.cleaned_data['name']
        return valid_name(name)

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        return valid_name(last_name)
    
    def clean_age(self):
        age = self.cleaned_data['age']
        return valid_age(age)