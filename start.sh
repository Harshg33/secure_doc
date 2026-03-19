#!/bin/bash
# SecureDoc AI — Quick Start Script

echo "🔐 SecureDoc AI — Starting up..."

# Check Python
if ! command -v python3 &> /dev/null; then
  echo "❌ Python 3 not found. Please install Python 3.9+."
  exit 1
fi

# Check .env
if [ ! -f backend/.env ]; then
  echo "⚠️  No .env file found. Copying from .env.example..."
  cp backend/.env.example backend/.env
  echo "📝 Please edit backend/.env and add your ANTHROPIC_API_KEY, then re-run this script."
  exit 1
fi

# Check API key is set
source backend/.env
if [[ "$ANTHROPIC_API_KEY" == "sk-ant-your-key-here" || -z "$ANTHROPIC_API_KEY" ]]; then
  echo "❌ Please set your ANTHROPIC_API_KEY in backend/.env"
  exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
cd backend
pip install -r requirements.txt -q

# Export env vars
export ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY

# Launch
echo ""
echo "✅ Starting SecureDoc AI backend..."
echo "🌐 Open your browser at: http://localhost:8000"
echo ""
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
