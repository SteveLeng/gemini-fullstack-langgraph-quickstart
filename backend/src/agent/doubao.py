import os
from openai import OpenAI

# Initialize Doubao (Ark) client
# Ensure you have stored your Ark API key in the ARK_API_KEY environment variable
doubao_client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.getenv("ARK_API_KEY"),
)

def call_doubao(formatted_prompt: str, model: str, temperature: float = 0, n: int = 1) -> str:
    """
    Call Doubao (Ark) API to generate a completion given a prompt.

    Args:
        formatted_prompt: The prompt string to send to Doubao.
        model: The Doubao model ID or endpoint.
        temperature: Sampling temperature.
        n: Number of completions to generate.

    Returns:
        The generated content as a string.
    """
    resp = doubao_client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": formatted_prompt}
                ],
            }
        ],
        temperature=temperature,
        n=n,
    )

    choice = resp.choices[0]
    raw = getattr(choice.message, "content", None) or getattr(choice, "content", None)
    if isinstance(raw, list):
        # Join all text segments if content is a list
        content = "".join(seg.get("text", "") for seg in raw if isinstance(seg, dict))
    else:
        content = str(raw)

    return content
