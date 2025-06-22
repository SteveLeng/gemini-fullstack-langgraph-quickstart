#!/usr/bin/env python3
"""
Test script for finalize_answer functionality with different LLM providers.
This script allows you to test the answer generation with Gemini, DouBao, or Qwen models.
"""

import os
import sys
from typing import Dict, Any, List
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from agent.llm_factory import LLMFactory
from agent.prompts import get_current_date, answer_instructions
from agent.utils import get_research_topic
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()


def create_mock_state() -> Dict[str, Any]:
    """Create a mock state for testing."""
    return {
        "messages": [
            HumanMessage(content="请介绍一下人工智能的发展历史")
        ],
        "web_research_result": [
            "人工智能（AI）是计算机科学的一个分支，旨在创建能够执行通常需要人类智能的任务的系统。\n\n"
            "AI的发展可以追溯到1950年代，当时艾伦·图灵提出了著名的图灵测试。1956年，在达特茅斯会议上，"
            "约翰·麦卡锡首次提出了'人工智能'这个术语。\n\n"
            "在接下来的几十年里，AI经历了几个发展阶段：\n"
            "1. 1950-1960年代：早期AI研究，重点是符号AI和逻辑推理\n"
            "2. 1970-1980年代：专家系统的发展\n"
            "3. 1990-2000年代：机器学习的兴起\n"
            "4. 2010年代至今：深度学习和神经网络的突破\n\n"
            "近年来，大型语言模型（如GPT、BERT等）的出现标志着AI技术的重大进步。"
        ],
        "sources_gathered": [
            {
                "short_url": "https://example1.com",
                "value": "https://en.wikipedia.org/wiki/Artificial_intelligence",
                "segments": ["AI definition", "Turing test"]
            },
            {
                "short_url": "https://example2.com", 
                "value": "https://www.britannica.com/technology/artificial-intelligence",
                "segments": ["AI history", "Dartmouth conference"]
            }
        ]
    }


def test_finalize_answer_with_model(model_name: str) -> None:
    """
    Test the finalize_answer functionality with a specific model.
    
    Args:
        model_name: The name of the model to test (e.g., 'gemini-2.0-flash', 'doubao-1.5', 'qwen-max')
    """
    print(f"\n{'='*60}")
    print(f"Testing with model: {model_name}")
    print(f"{'='*60}")
    
    try:
        # Create mock state
        state = create_mock_state()
        
        # Format the prompt
        current_date = get_current_date()
        formatted_prompt = answer_instructions.format(
            current_date=current_date,
            research_topic=get_research_topic(state["messages"]),
            summaries="\n---\n\n".join(state["web_research_result"]),
        )
        
        print(f"Research topic: {get_research_topic(state['messages'])}")
        print(f"Current date: {current_date}")
        print(f"\nPrompt length: {len(formatted_prompt)} characters")
        
        # Create LLM instance
        print(f"\nCreating LLM instance for {model_name}...")
        llm = LLMFactory.create_llm(
            model_name=model_name,
            temperature=0,
            max_retries=2,
        )
        
        # Generate the answer
        print("Generating answer...")
        result = llm.invoke(formatted_prompt)
        
        # Process the result (simulate the URL replacement logic)
        content = result.content
        unique_sources = []
        
        for source in state["sources_gathered"]:
            if source["short_url"] in content:
                content = content.replace(source["short_url"], source["value"])
                unique_sources.append(source)
        
        # Display results
        print(f"\nGenerated answer ({len(content)} characters):")
        print("-" * 40)
        print(content)
        print("-" * 40)
        
        print(f"\nSources used: {len(unique_sources)}")
        for i, source in enumerate(unique_sources, 1):
            print(f"  {i}. {source['value']}")
        
        print(f"\n✅ Test completed successfully for {model_name}")
        
    except Exception as e:
        print(f"\n❌ Error testing {model_name}: {str(e)}")
        print(f"Error type: {type(e).__name__}")


def main():
    """Main function to run the tests."""
    print("Finalize Answer Test Script")
    print("This script tests the answer generation with different LLM providers.")
    
    # Check environment variables
    print("\nChecking environment variables...")
    env_vars = {
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
        "DOUBAO_API_KEY": os.getenv("DOUBAO_API_KEY"), 
        "QIANFAN_API_KEY": os.getenv("QIANFAN_API_KEY"),
    }
    
    for var, value in env_vars.items():
        status = "✅ Set" if value else "❌ Not set"
        print(f"  {var}: {status}")
    
    # Define models to test
    models_to_test = []
    
    if env_vars["GEMINI_API_KEY"]:
        models_to_test.extend([
            "gemini-2.0-flash",
            "gemini-2.5-flash-preview-04-17",
            "gemini-2.5-pro-preview-05-06"
        ])
    
    if env_vars["DOUBAO_API_KEY"]:
        models_to_test.extend([
            "doubao-1.5",
            "doubao-1.5-pro", 
            "doubao-1.5-flash"
        ])
    
    if env_vars["QIANFAN_API_KEY"]:
        models_to_test.extend([
            "qwen-max",
            "qwen-plus",
            "qwen-turbo"
        ])
    
    if not models_to_test:
        print("\n❌ No API keys found. Please set at least one of the following:")
        print("  - GEMINI_API_KEY")
        print("  - DOUBAO_API_KEY") 
        print("  - QIANFAN_API_KEY")
        return
    
    print(f"\nModels to test: {', '.join(models_to_test)}")
    
    # Run tests
    for model in models_to_test:
        test_finalize_answer_with_model(model)
    
    print(f"\n{'='*60}")
    print("All tests completed!")
    print(f"{'='*60}")


if __name__ == "__main__":
    main() 