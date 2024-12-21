from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StoryBrainstormSerializer
from .models import StoryBrainstorm
import openai

@api_view(['POST'])
def submit_brainstorm(request):
    serializer = StoryBrainstormSerializer(data=request.data)
    if serializer.is_valid():
        story = serializer.save()
        
        # 构建提示词
        prompt = f"""
        Story Summary: {story.story_summary}
        Scenario Description: {story.scenario_description}
        
        Audience Roles:
        {chr(10).join([f"Role {role.order}: {role.description}" for role in story.audience_roles.all()])}
        
        Target Audience: {story.target_audience}
        """
        
        if story.classify_by_age:
            prompt += f"\nAge Range: {story.min_age} to {story.max_age} years old"
            
        # 添加具体的指导要求
        prompt += """
        
        Based on the above information, please provide:
        1. Three potential decision points that would be engaging for the target audience
        2. Analysis of how these decision points align with the audience roles
        3. Suggestions for making the story more interactive
        4. Potential challenges and how to address them
        """
        
        try:
            # 调用 OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant specializing in interactive storytelling and audience engagement."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            # 返回结果
            return Response({
                'story': serializer.data,
                'analysis': response.choices[0].message['content']
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': 'Error generating analysis',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_story(request, pk):
    try:
        story = StoryBrainstorm.objects.get(pk=pk)
        serializer = StoryBrainstormSerializer(story)
        return Response(serializer.data)
    except StoryBrainstorm.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
