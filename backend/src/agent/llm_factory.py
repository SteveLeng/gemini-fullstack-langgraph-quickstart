import os
from typing import Optional
from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_models import QianfanChatEndpoint
from langchain_community.chat_models import ChatZhipuAI
from langchain_community.chat_models import ChatByteDance


class LLMFactory:
    """Factory class for creating different LLM instances based on model name."""
    
    @staticmethod
    def create_llm(
        model_name: str,
        temperature: float = 0,
        max_retries: int = 2,
        api_key: Optional[str] = None
    ) -> BaseChatModel:
        """
        Create an LLM instance based on the model name.
        
        Args:
            model_name: The name of the model (e.g., 'gemini-2.0-flash', 'doubao-1.5', 'qwen-max')
            temperature: The temperature for generation
            max_retries: Maximum number of retries
            api_key: API key for the model provider
            
        Returns:
            BaseChatModel: The configured LLM instance
        """
        # Determine the provider from model name
        if model_name.startswith("gemini"):
            return LLMFactory._create_gemini_llm(model_name, temperature, max_retries, api_key)
        elif model_name.startswith("doubao"):
            return LLMFactory._create_doubao_llm(model_name, temperature, max_retries, api_key)
        elif model_name.startswith("qwen"):
            return LLMFactory._create_qwen_llm(model_name, temperature, max_retries, api_key)
        else:
            raise ValueError(f"Unsupported model: {model_name}")
    
    @staticmethod
    def _create_gemini_llm(
        model_name: str,
        temperature: float,
        max_retries: int,
        api_key: Optional[str]
    ) -> ChatGoogleGenerativeAI:
        """Create a Gemini LLM instance."""
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set")
        
        return ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            max_retries=max_retries,
            api_key=api_key,
        )
    
    @staticmethod
    def _create_doubao_llm(
        model_name: str,
        temperature: float,
        max_retries: int,
        api_key: Optional[str]
    ) -> ChatByteDance:
        """Create a DouBao (ByteDance) LLM instance."""
        api_key = api_key or os.getenv("DOUBAO_API_KEY")
        if not api_key:
            raise ValueError("DOUBAO_API_KEY is not set")
        
        # Map model names to DouBao model names
        model_mapping = {
            "doubao-1.5": "doubao-1.5",
            "doubao-1.5-pro": "doubao-1.5-pro",
            "doubao-1.5-flash": "doubao-1.5-flash",
        }
        
        doubao_model = model_mapping.get(model_name, "doubao-1.5")
        
        return ChatByteDance(
            model=doubao_model,
            temperature=temperature,
            max_retries=max_retries,
            api_key=api_key,
        )
    
    @staticmethod
    def _create_qwen_llm(
        model_name: str,
        temperature: float,
        max_retries: int,
        api_key: Optional[str]
    ) -> QianfanChatEndpoint:
        """Create a Qwen (Qianfan) LLM instance."""
        api_key = api_key or os.getenv("QIANFAN_API_KEY")
        if not api_key:
            raise ValueError("QIANFAN_API_KEY is not set")
        
        # Map model names to Qianfan model names
        model_mapping = {
            "qwen-max": "qwen-max",
            "qwen-plus": "qwen-plus", 
            "qwen-turbo": "qwen-turbo",
            "qwen-max-longcontext": "qwen-max-longcontext",
        }
        
        qianfan_model = model_mapping.get(model_name, "qwen-max")
        
        return QianfanChatEndpoint(
            qianfan_ak=api_key,
            model=qianfan_model,
            temperature=temperature,
            max_retries=max_retries,
        ) 