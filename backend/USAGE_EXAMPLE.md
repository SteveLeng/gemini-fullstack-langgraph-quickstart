# 多LLM提供商使用示例

## 快速开始

### 1. 安装依赖

```bash
cd backend
./install_dependencies.sh
```

### 2. 配置API密钥

在 `.env` 文件中添加你的API密钥：

```bash
# Google Gemini
GEMINI_API_KEY=your_gemini_api_key_here

# 豆包（字节跳动）
DOUBAO_API_KEY=your_doubao_api_key_here

# 通义千问（千帆）
QIANFAN_API_KEY=your_qianfan_api_key_here
```

### 3. 简单测试

运行简单示例来验证安装：

```bash
python example_multi_llm.py
```

### 4. 完整测试

运行完整的finalize_answer功能测试：

```bash
python test_finalize_answer.py
```

## 代码示例

### 基本使用

```python
from agent.llm_factory import LLMFactory

# 创建不同提供商的LLM实例
gemini_llm = LLMFactory.create_llm("gemini-2.0-flash")
doubao_llm = LLMFactory.create_llm("doubao-1.5")
qwen_llm = LLMFactory.create_llm("qwen-max")

# 使用LLM
prompt = "请解释什么是机器学习？"
result = doubao_llm.invoke(prompt)
print(result.content)
```

### 在LangGraph中使用

修改 `configuration.py` 中的默认模型：

```python
answer_model: str = Field(
    default="doubao-1.5",  # 改为你想要的模型
    metadata={
        "description": "The name of the language model to use for the agent's answer."
    },
)
```

## 支持的模型列表

### Google Gemini
- `gemini-2.0-flash` - 快速且经济
- `gemini-2.5-flash-preview-04-17` - 平衡性能和速度
- `gemini-2.5-pro-preview-05-06` - 最高性能

### 豆包（DouBao/ByteDance）
- `doubao-1.5` - 豆包1.5
- `doubao-1.5-pro` - 豆包1.5 Pro
- `doubao-1.5-flash` - 豆包1.5 Flash

### 通义千问（Qwen/Qianfan）
- `qwen-max` - 最高性能
- `qwen-plus` - 平衡版本
- `qwen-turbo` - 快速版本
- `qwen-max-longcontext` - 长上下文版本

## 故障排除

### 常见问题

1. **导入错误**
   ```
   ModuleNotFoundError: No module named 'langchain_community'
   ```
   解决：运行 `pip install langchain-community`

2. **API密钥错误**
   ```
   ValueError: DOUBAO_API_KEY is not set
   ```
   解决：在 `.env` 文件中设置正确的API密钥

3. **模型名称错误**
   ```
   ValueError: Unsupported model: unknown-model
   ```
   解决：使用支持的模型名称

### 获取API密钥

- **豆包**: 访问 [字节跳动AI开放平台](https://ai.bytedance.com/)
- **通义千问**: 访问 [千帆大模型平台](https://cloud.baidu.com/product/wenxinworkshop)
- **Gemini**: 访问 [Google AI Studio](https://aistudio.google.com/) 