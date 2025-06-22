#!/usr/bin/env python3
"""
验证豆包API配置的脚本
"""

import os
import sys
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Load environment variables
load_dotenv()

def verify_doubao_config():
    """验证豆包API配置"""
    print("豆包API配置验证")
    print("=" * 50)
    
    # 检查环境变量
    doubao_api_key = os.getenv("DOUBAO_API_KEY")
    if not doubao_api_key:
        print("❌ DOUBAO_API_KEY 未设置")
        print("请在 .env 文件中设置 DOUBAO_API_KEY")
        return False
    
    print(f"✅ DOUBAO_API_KEY 已设置: {doubao_api_key[:10]}...")
    
    # 检查依赖
    try:
        from langchain_community.chat_models import ChatByteDance
        print("✅ langchain_community 已安装")
    except ImportError:
        print("❌ langchain_community 未安装")
        print("请运行: pip install langchain-community")
        return False
    
    try:
        import bytedance
        print("✅ bytedance 包已安装")
    except ImportError:
        print("❌ bytedance 包未安装")
        print("请运行: pip install bytedance")
        return False
    
    # 测试LLM工厂
    try:
        from agent.llm_factory import LLMFactory
        print("✅ LLMFactory 导入成功")
        
        # 尝试创建豆包LLM实例
        llm = LLMFactory.create_llm("doubao-1.5")
        print("✅ 豆包LLM实例创建成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建豆包LLM实例失败: {str(e)}")
        return False

def test_doubao_models():
    """测试豆包支持的模型"""
    print("\n豆包支持的模型:")
    print("-" * 30)
    
    models = [
        "doubao-1.5",
        "doubao-1.5-pro", 
        "doubao-1.5-flash"
    ]
    
    for model in models:
        try:
            from agent.llm_factory import LLMFactory
            llm = LLMFactory.create_llm(model)
            print(f"✅ {model} - 配置成功")
        except Exception as e:
            print(f"❌ {model} - 配置失败: {str(e)}")

def main():
    """主函数"""
    print("豆包API配置验证工具")
    print("=" * 50)
    
    # 验证配置
    if verify_doubao_config():
        print("\n🎉 豆包API配置验证通过!")
        
        # 测试支持的模型
        test_doubao_models()
        
        print("\n📝 下一步:")
        print("1. 运行简单测试: python example_multi_llm.py")
        print("2. 运行完整测试: python test_finalize_answer.py")
    else:
        print("\n❌ 豆包API配置验证失败!")
        print("请检查上述错误并修复后重试")

if __name__ == "__main__":
    main() 