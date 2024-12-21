from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from .models import ChatMessage
import json
import time
import base64
import os
import ollama
from openai import OpenAI

from config.settings import (
    MOONSHOT_API_KEY, 
    MOONSHOT_BASE_URL, 
    MOONSHOT_MODEL,
    MOONSHOT_TEMPERATURE,
    OLLAMA_MODEL,
    OLLAMA_VISION_MODEL
)

def handle_uploaded_image(image_data):
    """处理上传的图片"""
    try:
        # 解码base64图片数据
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        
        # 生成文件名
        filename = f"chat_image_{time.time()}.{ext}"
        
        # 确保目录存在
        os.makedirs('media/chat_images', exist_ok=True)
        
        # 保存图片
        data = base64.b64decode(imgstr)
        with default_storage.open(f'chat_images/{filename}', 'wb') as f:
            f.write(data)
            
        return f'media/chat_images/{filename}'
    except Exception as e:
        print(f"Error handling image: {e}")
        return None

def generate_response(message, image_path=None, history=None):
    try:
        messages = []
        if history:
            for msg in history:
                messages.append({
                    'role': msg.role,
                    'content': msg.content
                })
        
        current_message = {
            'role': 'user',
            'content': message
        }
        
        if image_path:
            with open(image_path, 'rb') as img_file:
                img_bytes = img_file.read()
                response = ollama.chat(
                    model=OLLAMA_VISION_MODEL,
                    messages=[{
                        'role': 'system',
                        'content': f"这是历史消息，仅供参考，不用输出对其中问题的回答！：{messages}"
                    },
                    {
                        'role': 'user',
                        'content': message,
                        'images': [img_bytes]
                    }]
                )
        else:
            response = ollama.chat(
                model=OLLAMA_MODEL,
                messages=[{
                    'role': 'system',
                    'content': f"这是历史消息,仅供参考，不用输出对其中问题的回答！：{messages}"
                },
                {
                    'role': 'user',
                    'content': message,
                }]
            )
            
        for char in response['message']['content']:
            yield char
            time.sleep(0.02)
    except Exception as e:
        print(f"Error generating response: {e}")
        yield "抱歉，生成响应时出现错误。"

def stream_response(message, image_data=None):
    """生成SSE格式的响应"""
    try:
        # 处理图片上传
        image_path = None
        if image_data:
            image_path = handle_uploaded_image(image_data)
        
        # 获取最近的聊天历史（最多10条），使用 timestamp 而不是 created_at
        history = ChatMessage.objects.order_by('-timestamp')[:100]
        
        # 保存用户消息
        user_message = ChatMessage.objects.create(
            role='user',
            content=message,
            image=image_path if image_path else None
        )
        
        # 发送连接成功消息
        yield "data: {}\n\n".format(json.dumps({
            "type": "connected",
            "message": "连接成功"
        }))
        
        # 生成并流式发送AI响应
        response_text = ""
        for char in generate_response(message, image_path, history):
            response_text += char
            data = json.dumps({
                "type": "message",
                "response": response_text
            })
            yield f"data: {data}\n\n"
        
        # 保存AI响应
        ChatMessage.objects.create(
            role='assistant',
            content=response_text
        )
        
        # 发送完成消息
        yield "data: {}\n\n".format(json.dumps({
            "type": "done",
            "message": "响应完成"
        }))
        
    except Exception as e:
        yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def chat(request):
    """处理聊天请求"""
    if request.method == 'OPTIONS':
        response = StreamingHttpResponse()
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        image = data.get('image', None)
        
        response = StreamingHttpResponse(
            streaming_content=stream_response(message, image),
            content_type='text/event-stream'
        )
        
        # 设置响应头
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"
        
        return response
        
    except Exception as e:
        print(f"Error processing request: {e}")
        response = StreamingHttpResponse(
            streaming_content=[f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"],
            content_type='text/event-stream'
        )
        response["Access-Control-Allow-Origin"] = "*"
        return response

@csrf_exempt
@require_http_methods(["POST"])
def clear_history(request):
    """清空聊天历史记录"""
    try:
        # 删除所有聊天记录
        ChatMessage.objects.all().delete()
        
        return JsonResponse({
            'status': 'success',
            'message': '历史记录已清空'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
