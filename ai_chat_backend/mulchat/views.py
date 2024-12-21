from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import time
import ollama
import pandas as pd
from openai import OpenAI
import os

from config.settings import (
    MOONSHOT_API_KEY, 
    MOONSHOT_BASE_URL, 
    MOONSHOT_MODEL,
    MOONSHOT_TEMPERATURE,
    OLLAMA_MODEL
)


# 获取当前文件所在目录的路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 构建 memory_data.json 的路径
json_path = os.path.join(BASE_DIR, 'memory_data.json')

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

def read_memory_data():
    """
    读取记忆数据JSON文件
    返回解析后的JSON数据
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print('找不到记忆数据文件')
        return None
    except json.JSONDecodeError:
        print('JSON文件格式错误')
        return None
    except Exception as e:
        print(f'读取文件时发生错误: {str(e)}')
        return None
    
def kimi():
    client = OpenAI(
        api_key=MOONSHOT_API_KEY,
        base_url=MOONSHOT_BASE_URL,
    )
 
    completion = client.chat.completions.create(
        model=MOONSHOT_MODEL,
        messages=[
            {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手..."},
            {"role": "user", "content": "你好，我叫李雷，1+1等于多少？"}
        ],
        temperature=MOONSHOT_TEMPERATURE,
    )
 
    return completion.choices[0].message.content
# AI 角色配置
AI_ROLES = [
    {
        'name': 'John',
        'personality': 'Key_Extractor',
        'prefix': 'Hi! I am Jhon, the keywords of your question is:'
    },
    {
        'name': 'Lisa', 
        'personality': 'Key_Memory_Recaller',
        'prefix': 'Hi! I am Lisa, the key memory of this guy is:'
    },
    {
        'name': 'Maha',
        'personality': 'Answer_Generator',
        'prefix': 'Hi! I am Maha, the answer of this guy is:'
    }
]

def generate_ai_response(message, ai_index, previous_responses=None):
    """生成AI回复的工作流"""
    ai_role = AI_ROLES[ai_index]
    client = OpenAI(
    api_key = "sk-keu02yi33iJM5cseCbnHAQvl1uyWpRcv4TQmFzTiBAN7Z7kR",
    base_url = "https://api.moonshot.cn/v1",
)
    if ai_index == 0:  # John: 专业分析
        completion = client.chat.completions.create(
        model = "moonshot-v1-8k",
        messages = [
            {"role": "system", "content": "请根据用户输入的语句提取关键词，时间地点人物，并输出关键字。输出例子：19号晚上10点，图书馆，刘琳。请严格按照输出例子格式输出，日期可分为几号几点，例如十八号早上十点，请不要只输出几号，不要输出任何其他信息！！！如果时间地点人物没有完全提取到，请只输出提取到的关键信息！！！不要自己瞎造数据"},
        {"role": "user", "content": message}
    ],
        temperature = 0.3,
    )
    #     response = ollama.chat(
    #     model='llama3.2',
    #     messages=[{
    #         'role': 'system',
    #         'content': "请根据用户输入的语句提取关键词，时间地点人物，并输出关键字。输出例子：19号晚上10点，图书馆，刘琳。请严格按照输出例子格式输出，日期可分为几号几点，例如十八号早上十点，请不要只输出几号，不要输出任何其他信息！！！如果时间地点人物没有完全提取到，请只输出提取到的关键信息！！！不要自己瞎造数据"
    #     },{
    #         'role': 'user',
    #         'content': message
    #     }]
    # )
        response = f"{ai_role['prefix']}\n\nkeywords: {completion.choices[0].message.content}"
        #response = f"{ai_role['prefix']}{message}"
    elif ai_index == 1:  # Lisa: 创意思考
        john_analysis = previous_responses[0].split("keywords: ")[1]
        # 读取记忆数据
        data = read_memory_data()
        print(data['characters']['林小美'])
        lin_xiao_mei = data['characters']['林小美']
        keywords = john_analysis
        print(john_analysis)
        completion = client.chat.completions.create(
        model = "moonshot-v1-8k",
        messages = [
            {"role": "system", "content": f"这是林小美记忆的json文件{lin_xiao_mei}，请根据关键词搜索出具体的json数据。并输出相关具体json数据,例如关键词是21号下午，艺术社活动室，你就要寻找21号的相关事件。如果时间地点对不上，请根据自己的记忆输出关联信息"},
        {"role": "user", "content": f"这是问题的关键词:{keywords}"}
    ],
        temperature = 0.3,
    )
    #     response = ollama.chat(
    #     model='llama3.2',
    #     messages=[{
    #         'role': 'assistant',
    #         'content': f"这是林小美记忆的json文件{lin_xiao_mei}，请根据关键词搜索出具体的json数据。并输出相关具体json数据\
    #             例如关键词是21号下午，艺术社活动室，你就要寻找21号的相关事件。如果时间地点对不上，请根据自己的记忆输出关联信息"
    #     },{
    #         'role': 'user',
    #         'content': f"这是问题:{message}这是问题的关键词:{keywords}"
    #     }]
    # )
        response = f"{ai_role['prefix']}\n\nkey_memory: {completion.choices[0].message.content}"
    else:  # Maha: 整合总结
        john_analysis = previous_responses[0]
        keywords = john_analysis.split("keywords: ")[1]
        lisa_ideas = previous_responses[1]
        print(lisa_ideas)
        key_memory = lisa_ideas.split("key_memory: ")[1]
        data = read_memory_data()
        lin_xiao_mei = data['characters']['林小美']
        completion = client.chat.completions.create(
        model = "moonshot-v1-8k",
        messages = [
            {"role": "system", "content": f"你叫林小美，今年20岁，是江城大学的学生，你跟刘琳是好朋友，你俩亲密无间。这是用户问题的关键词:{keywords}。这是当天的关键记忆:{key_memory}。这是你所有的记忆:{lin_xiao_mei}，请根据用户问题输出纯中文回答.\
                如果记忆跟问题不符合，请进行辩驳并输出正确的记忆。例如你根本没有在二十号晚上跟刘琳在一起聊天，而用户问了你这样的问题，请辩驳。请纯中文回答"},
        {"role": "user", "content": message}
    ],
        temperature = 0.3,
    )
    #     result = ollama.chat(
    #     model='llama3.2',
    #     messages=[{
    #         'role': 'assistant',
    #         'content': f"你叫林小美，今年20岁，是江城大学的学生，你跟刘琳是好朋友，你俩亲密无间。这是用户问题的关键词:{keywords}。这是当天的关键记忆:{key_memory}。这是你所有的记忆:{lin_xiao_mei}，请根据用户问题输出纯中文回答.\
    #             如果记忆跟问题不符合，请进行辩驳并输出正确的记忆。例如你根本没有在二十号晚上跟刘琳在一起聊天，而用户问了你这样的问题，请辩驳。请纯中文回答"
    #     },{
    #         'role': 'user',
    #         'content': message
    #     }]
    # )
        response = f"{ai_role['prefix']}\n\n{completion.choices[0].message.content}"
    
    # 确保每个字符都能被单独发送
    for char in response:
        yield char

@csrf_exempt
@require_http_methods(["GET", "POST", "OPTIONS"])
def multi_chat(request):
    """处理多AI聊天请求"""
    if request.method == 'OPTIONS':
        response = StreamingHttpResponse()
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    try:
        # 从请求体中获取消息
        data = json.loads(request.body)
        message = data.get('message', '')
        
        def stream_response():
            try:
                ai_responses = []

                for i in range(len(AI_ROLES)):
                    yield "data: {}\n\n".format(json.dumps({
                        "type": "start",
                        "aiIndex": i,
                        "message": f"{AI_ROLES[i]['name']} 开始回复"
                    }))

                    response = generate_ai_response(message, i, ai_responses)
                    current_response = ""
                    
                    for char in response:
                        current_response += char
                        yield "data: {}\n\n".format(json.dumps({
                            "type": "token",
                            "aiIndex": i,
                            "token": char
                        }))
                        time.sleep(0.05)
                    
                    ai_responses.append(current_response)
                    
                    yield "data: {}\n\n".format(json.dumps({
                        "type": "end",
                        "aiIndex": i,
                        "message": f"{AI_ROLES[i]['name']} 回复完成"
                    }))
                    
                    time.sleep(0.05)
                
                yield "data: {}\n\n".format(json.dumps({
                    "type": "done",
                    "message": "所有AI回复完成"
                }))
                
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
        
        response = StreamingHttpResponse(
            streaming_content=stream_response(),
            content_type='text/event-stream'
        )
        
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"
        
        return response
        
    except Exception as e:
        response = StreamingHttpResponse(
            streaming_content=[f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"],
            content_type='text/event-stream'
        )
        response["Access-Control-Allow-Origin"] = "*"
        return response
