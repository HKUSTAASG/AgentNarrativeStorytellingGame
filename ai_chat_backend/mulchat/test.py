import json
import ollama
def read_memory_data():
    """
    读取记忆数据JSON文件
    返回解析后的JSON数据
    """
    try:
        with open('test/ai_chat_backend/mulchat/memory_data.json', 'r', encoding='utf-8') as f:
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
def Agent_1():
    response = ollama.chat(
        model='llama3.2',
        messages=[{
            'role': 'system',
            'content': "请根据用户输入的语句提取关键词，时间地点人物，并输出关键字。输出例子：19号晚上10点，图书馆，刘琳。请严格按照输出例子格式输出，不要输出任何其他信息！！！"
        },{
            'role': 'user',
            'content': "你好林小美，能不能告诉我21号的晚上你跟刘琳在宿舍楼下聊些什么？根据监控你俩的面孔有些许疑惑和紧张。"
        }]
    )
    return response['message']['content']
def Agent_2():
    question = "你好林小美，能不能告诉我21号的晚上你跟刘琳在宿舍楼下聊些什么？根据监控你俩的面孔有些许疑惑和紧张。"
    with open('test/ai_chat_backend/mulchat/memory_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    lin_xiao_mei = data['characters']['林小美']
    question_keywords = Agent_1()
    print(question_keywords)
    response = ollama.chat(
        model='llama3.2',
        messages=[{
            'role': 'assistant',
            'content': f"这是林小美记忆的json文件{lin_xiao_mei}，请根据agent_1提供的关键词搜索出具体的json数据路径。并输出相关具体json数据\
                例如关键词是21号下午，艺术社活动室，你就要寻找21号的相关事件。如果时间地点对不上，请根据自己的记忆输出关联信息"
        },{
            'role': 'user',
            'content': f"这是agent_1的关键词{question_keywords},请根据时间地点人物这些关键词找出具体事件，请严格输出具体信息，不要输出任何其他信息！！！"
        }]
    )
    return response['message']['content']
def Agent_3():
    question = "你好林小美，能不能告诉我21号的晚上你跟刘琳在宿舍楼下聊些什么？根据监控你俩的面孔有些许疑惑和紧张。"
    with open('test/ai_chat_backend/mulchat/memory_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    lin_xiao_mei = data['characters']['林小美']
    key_memory = Agent_2()
    # 将字符串形式的路径转换为实际的内存访问
    print(key_memory)
    question_keywords = Agent_1()
    memories = Agent_2()
    response = ollama.chat(
        model='llama3.2',
        messages=[{
            'role': 'assistant',
            'content': f"你叫林小美，今年20岁，是江城大学的学生，你跟刘琳是好朋友，你俩亲密无间。这是用户问题的关键词:{question_keywords}。这是当天的关键记忆:{key_memory}。这是你所有的记忆:{lin_xiao_mei}，请根据用户问题输出纯中文回答.\
                如果记忆跟问题不符合，请进行辩驳并输出正确的记忆。例如你根本没有在二十号晚上跟刘琳在一起聊天，而用户问了你这样的问题，请辩驳。"
        },{
            'role': 'user',
            'content': question
        }]
    )
    return response['message']['content']
data = read_memory_data()
print(Agent_3())
