from django.db import models

class StoryBrainstorm(models.Model):
    story_summary = models.CharField(max_length=500)
    scenario_description = models.TextField()
    target_audience = models.TextField()
    classify_by_age = models.BooleanField(default=False)
    min_age = models.IntegerField(null=True, blank=True)
    max_age = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Story: {self.story_summary[:50]}..."

class AudienceRole(models.Model):
    story = models.ForeignKey(StoryBrainstorm, related_name='audience_roles', on_delete=models.CASCADE)
    description = models.TextField()
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Role {self.order} for Story {self.story.id}"
