# Sharp School: AI Agent Narrative Storytelling Game 


An interactive AI chat application built with Vue.js and Django, featuring multi-model conversations, game interactions, and brainstorming tools.

## Prerequisites

- Anaconda or Miniconda
- Node.js 16+
- Ollama (for local AI models)
- Git

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/HKUSTAASG/AgentNarrativeStorytellingGame.git
cd AgentNarrativeStorytellingGame
```

### 2. Backend Setup
```bash
# Create and activate Conda environment
conda create -n ai-chat python=3.9
conda activate ai-chat

# Install backend dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env.development
# Edit .env.development with your API keys

# Initialize database
python manage.py migrate
python manage.py runserver
```

### 3. Frontend Setup
```bash
# Install frontend dependencies
cd ../ai-chat-frontend
npm install
npm run serve
```

### 4. Clone StorytellingAgent
To run the StorytellingAgent Game, you need to clone the StorytellingAgent repository and run the related code following the instructions in the repository.

```bash
git clone https://github.com/MPX0222/StorytellingAgent.git
cd StorytellingAgent
```

## Environment Variables (.env.development)
```bash
MOONSHOT_API_KEY=your_moonshot_api_key
MOONSHOT_BASE_URL=https://api.moonshot.cn/v1
MOONSHOT_MODEL=moonshot-v1-8k
OLLAMA_MODEL=llama3.2
OLLAMA_VISION_MODEL=llama3.2-vision
OPENAI_API_KEY=your_openai_api_key
```

## Access Points
For this project, you can access the following points:
- Frontend: http://localhost:8080
- Backend API: http://localhost:9000

For the StorytellingAgent Game, you can access the following points:
- Frontend: http://localhost:5073
- Backend API: http://localhost:8000






