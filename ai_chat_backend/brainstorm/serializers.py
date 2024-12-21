from rest_framework import serializers
from .models import StoryBrainstorm, AudienceRole

class AudienceRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudienceRole
        fields = ['description', 'order']

class StoryBrainstormSerializer(serializers.ModelSerializer):
    audience_roles = AudienceRoleSerializer(many=True)

    class Meta:
        model = StoryBrainstorm
        fields = ['id', 'story_summary', 'scenario_description', 'audience_roles',
                 'target_audience', 'classify_by_age', 'min_age', 'max_age']

    def create(self, validated_data):
        audience_roles_data = validated_data.pop('audience_roles')
        story = StoryBrainstorm.objects.create(**validated_data)
        
        for role_data in audience_roles_data:
            AudienceRole.objects.create(story=story, **role_data)
        
        return story 