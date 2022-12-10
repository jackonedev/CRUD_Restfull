from rest_framework.serializers import ModelSerializer

from ..models import Profile

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ('personal_id', 'name', 'last_name', 'age')