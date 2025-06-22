#!/bin/bash

# Install script for multi-LLM provider dependencies

echo "Installing dependencies for multi-LLM provider support..."

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi

# Install new dependencies
echo "📦 Installing new dependencies..."

# Install zhipuai for ZhipuAI support
echo "Installing zhipuai..."
pip install zhipuai

# Install dashscope for Qwen support
echo "Installing dashscope..."
pip install dashscope

# Install bytedance for DouBao support
echo "Installing bytedance..."
pip install bytedance

# Install langchain-community if not already installed
echo "Installing langchain-community..."
pip install langchain-community

# Install the project in development mode
echo "Installing project in development mode..."
pip install -e .

echo "✅ Dependencies installed successfully!"
echo ""
echo "📝 Next steps:"
echo "1. Set up your API keys in .env file:"
echo "   - GEMINI_API_KEY for Google Gemini"
echo "   - DOUBAO_API_KEY for DouBao (ByteDance)"
echo "   - QIANFAN_API_KEY for Qwen (Qianfan)"
echo ""
echo "2. Test the installation:"
echo "   python example_multi_llm.py"
echo ""
echo "3. Run the full test:"
echo "   python test_finalize_answer.py" 