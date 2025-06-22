# 多LLM提供商支持 - Finalize Answer功能

这个项目现在支持使用多种LLM提供商来生成最终的答案，包括Google Gemini、豆包（DouBao）和通义千问（Qwen）。

## 支持的模型

### Google Gemini
- `gemini-2.0-flash`
- `gemini-2.5-flash-preview-04-17`
- `gemini-2.5-pro-preview-05-06`

### 豆包（DouBao/ByteDance）
- `doubao-1.5` (豆包1.5)
- `doubao-1.5-pro` (豆包1.5 Pro)
- `doubao-1.5-flash` (豆包1.5 Flash)

### 通义千问（Qwen/Qianfan）
- `qwen-max`
- `qwen-plus`
- `qwen-turbo`
- `qwen-max-longcontext`

## 环境变量配置

在 `.env` 文件中设置相应的API密钥：

```bash
# Google Gemini
GEMINI_API_KEY=your_gemini_api_key_here

# 豆包（字节跳动）
DOUBAO_API_KEY=your_doubao_api_key_here

# 通义千问（千帆）
QIANFAN_API_KEY=your_qianfan_api_key_here
```

## 安装依赖

```bash
# 安装新的依赖包
pip install bytedance dashscope langchain-community
```

或者使用项目的依赖管理：

```bash
# 在backend目录下
pip install -e .
```

## 使用方法

### 1. 在代码中使用

```python
from agent.llm_factory import LLMFactory

# 创建LLM实例
llm = LLMFactory.create_llm(
    model_name="doubao-1.5",  # 或 "qwen-max", "gemini-2.0-flash"
    temperature=0,
    max_retries=2,
)

# 使用LLM
result = llm.invoke("你的提示词")
print(result.content)
```

### 2. 在LangGraph中使用

在 `finalize_answer` 函数中，模型会自动根据配置选择：

```python
# 在configuration.py中设置默认模型
answer_model: str = Field(
    default="doubao-1.5",  # 可以改为任何支持的模型
    metadata={
        "description": "The name of the language model to use for the agent's answer."
    },
)
```

### 3. 单独测试

运行测试脚本来验证不同模型的效果：

```bash
cd backend
python test_finalize_answer.py
```

这个脚本会：
- 检查环境变量配置
- 自动测试所有可用的模型
- 显示生成的结果和使用的源链接
- 报告任何错误

## 测试脚本功能

`test_finalize_answer.py` 脚本提供了以下功能：

1. **环境检查**: 自动检查API密钥是否配置
2. **多模型测试**: 根据可用的API密钥自动测试相应的模型
3. **结果展示**: 显示生成的答案、字符数和使用的源链接
4. **错误处理**: 详细的错误报告和异常处理

### 运行测试

```bash
# 确保在backend目录下
cd backend

# 设置环境变量（如果还没有设置）
export GEMINI_API_KEY="your_key"
export DOUBAO_API_KEY="your_key"
export QIANFAN_API_KEY="your_key"

# 运行测试
python test_finalize_answer.py
```

### 测试输出示例

```
Finalize Answer Test Script
This script tests the answer generation with different LLM providers.

Checking environment variables...
  GEMINI_API_KEY: ✅ Set
  DOUBAO_API_KEY: ✅ Set
  QIANFAN_API_KEY: ❌ Not set

Models to test: gemini-2.0-flash, gemini-2.5-flash-preview-04-17, gemini-2.5-pro-preview-05-06, doubao-1.5, doubao-1.5-pro, doubao-1.5-flash

============================================================
Testing with model: gemini-2.0-flash
============================================================
Research topic: 人工智能的发展历史
Current date: 2024年12月19日

Prompt length: 1234 characters

Creating LLM instance for gemini-2.0-flash...
Generating answer...

Generated answer (567 characters):
----------------------------------------
人工智能（AI）的发展历史可以追溯到1950年代...
----------------------------------------

Sources used: 2
  1. https://en.wikipedia.org/wiki/Artificial_intelligence
  2. https://www.britannica.com/technology/artificial-intelligence

✅ Test completed successfully for gemini-2.0-flash
```

## 注意事项

1. **API密钥**: 确保设置了正确的API密钥，否则相应的模型将无法使用
2. **模型映射**: 豆包模型名称直接对应豆包API的模型名称
3. **错误处理**: 如果某个模型不可用，测试脚本会跳过该模型并继续测试其他模型
4. **成本考虑**: 不同模型的API调用成本可能不同，请根据需求选择合适的模型

## 故障排除

### 常见错误

1. **API密钥未设置**
   ```
   ❌ Error testing doubao-1.5: DOUBAO_API_KEY is not set
   ```
   解决：在 `.env` 文件中设置相应的API密钥

2. **模型名称不支持**
   ```
   ❌ Error testing unknown-model: Unsupported model: unknown-model
   ```
   解决：使用支持的模型名称

3. **网络连接问题**
   ```
   ❌ Error testing qwen-max: Connection timeout
   ```
   解决：检查网络连接和API服务状态

### 获取API密钥

- **豆包**: 访问 [字节跳动AI开放平台](https://ai.bytedance.com/) 注册并获取API密钥
- **通义千问**: 访问 [千帆大模型平台](https://cloud.baidu.com/product/wenxinworkshop) 注册并获取API密钥
- **Gemini**: 访问 [Google AI Studio](https://aistudio.google.com/) 获取API密钥 