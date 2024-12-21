import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API Keys
MOONSHOT_API_KEY = os.getenv('MOONSHOT_API_KEY')
MOONSHOT_BASE_URL = os.getenv('MOONSHOT_BASE_URL', 'https://api.moonshot.cn/v1')

# Model Configurations
MOONSHOT_MODEL = os.getenv('MOONSHOT_MODEL', 'moonshot-v1-8k')
MOONSHOT_TEMPERATURE = float(os.getenv('MOONSHOT_TEMPERATURE', '0.3'))

# Ollama Configurations
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.2')
OLLAMA_VISION_MODEL = os.getenv('OLLAMA_VISION_MODEL', 'llama3.2-vision')
OLLAMA_API_BASE = os.getenv('OLLAMA_API_BASE', 'http://localhost:11434')

# OpenAI Configurations
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo') 