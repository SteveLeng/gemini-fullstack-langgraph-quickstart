#!/usr/bin/env python3
"""
Simple example demonstrating how to use different LLM providers.
"""

import os
import sys
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from agent.llm_factory import LLMFactory

# Load environment variables
load_dotenv()


def simple_test(model_name: str, prompt: str) -> None:
    """
    Simple test function to demonstrate LLM usage.
    
    Args:
        model_name: The name of the model to use
        prompt: The prompt to send to the model
    """
    print(f"\n{'='*50}")
    print(f"Testing: {model_name}")
    print(f"{'='*50}")
    
    try:
        # Create LLM instance
        llm = LLMFactory.create_llm(
            model_name=model_name,
            temperature=0.7,
            max_retries=2,
        )
        
        # Send prompt
        print(f"Prompt: {prompt}")
        print("\nGenerating response...")
        
        result = llm.invoke(prompt)
        
        print(f"\nResponse ({len(result.content)} characters):")
        print("-" * 30)
        print(result.content)
        print("-" * 30)
        
        print(f"✅ Success with {model_name}")
        
    except Exception as e:
        print(f"❌ Error with {model_name}: {str(e)}")


def main():
    """Main function."""
    print("Multi-LLM Provider Example")
    print("This example demonstrates how to use different LLM providers.")
    
    # Test prompt
    test_prompt = "请用一句话解释什么是人工智能？"
    
    # Available models (based on environment variables)
    available_models = []
    
    if os.getenv("GEMINI_API_KEY"):
        available_models.append("gemini-2.0-flash")
    
    if os.getenv("DOUBAO_API_KEY"):
        available_models.append("doubao-1.5")
    
    if os.getenv("QIANFAN_API_KEY"):
        available_models.append("qwen-max")
    
    if not available_models:
        print("\n❌ No API keys found. Please set at least one API key:")
        print("  - GEMINI_API_KEY")
        print("  - DOUBAO_API_KEY")
        print("  - QIANFAN_API_KEY")
        return
    
    print(f"\nAvailable models: {', '.join(available_models)}")
    
    # Test each available model
    for model in available_models:
        simple_test(model, test_prompt)
    
    print(f"\n{'='*50}")
    print("Example completed!")
    print(f"{'='*50}")


if __name__ == "__main__":
    main() 