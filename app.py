# IntelliChat AI Assistant - Gradio app for Hugging Face Spaces
#
# Deployment steps for Hugging Face Spaces:
# Step 1: Go to https://huggingface.co/spaces and click "Create new Space"
# Step 2: Name it "intellichat-ai-assistant", choose Gradio SDK
# Step 3: Upload all 4 files (app.py, requirements.txt, README.md, .env.example)
# Step 4: Go to Space Settings -> Variables and Secrets
# Step 5: Add Secret: Name=HF_TOKEN, Value=<your HF token from hf.co/settings/tokens>
# Step 6: Space auto-builds and launches — share the URL!

import os
from typing import Generator

import gradio as gr
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

SYSTEM_PROMPT = """You are IntelliChat, a helpful, harmless, and honest AI assistant. 
You provide clear, accurate, and thoughtful responses. You are friendly 
and concise. If you don't know something, you say so honestly."""

PRIMARY_MODEL_ID = "Qwen/Qwen2-7B-Instruct"
FALLBACK_MODEL_ID = "microsoft/Phi-2"
COMPATIBLE_FALLBACK_MODELS = [
    "Qwen/Qwen2.5-7B-Instruct",
    "meta-llama/Llama-3.1-8B-Instruct",
]

HF_TOKEN = os.environ.get("HF_TOKEN", "")
client = InferenceClient(model=PRIMARY_MODEL_ID, token=HF_TOKEN)
fallback_client = InferenceClient(model=FALLBACK_MODEL_ID, token=HF_TOKEN)

# Optional override for the primary model, e.g., MODEL_ID=microsoft/Phi-2.
MODEL_ID = os.environ.get("MODEL_ID", "").strip()
if MODEL_ID:
    client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)


def stream_chat_reply(
    inference_client: InferenceClient,
    messages: list[dict],
    max_tokens: int,
    temperature: float,
    top_p: float,
) -> Generator[str, None, None]:
    """Stream incremental assistant text from HF conversational API."""
    stream = inference_client.chat.completions.create(
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        stream=True,
    )

    response = ""
    for chunk in stream:
        piece = ""

        if hasattr(chunk, "choices") and chunk.choices:
            delta = getattr(chunk.choices[0], "delta", None)
            content = getattr(delta, "content", None)
            if isinstance(content, str):
                piece = content
            elif isinstance(content, list):
                piece = "".join(
                    str(item.get("text", ""))
                    for item in content
                    if isinstance(item, dict)
                )
        elif isinstance(chunk, str):
            piece = chunk

        if piece:
            response += piece
            yield response


CUSTOM_CSS = """
body, .gradio-container {
    background: #0b0f14 !important;
    color: #e5e7eb !important;
}

#app-shell {
    max-width: 1140px;
    margin: 18px auto;
    border-radius: 18px;
    box-shadow: 0 20px 48px rgba(0, 0, 0, 0.45);
    overflow: hidden;
    background: #111827;
    border: 1px solid #1f2937;
}

#header-banner {
    background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
    color: #f8fafc;
    padding: 20px 24px;
    border-bottom: 1px solid #1f2937;
}

#header-banner h1 {
    margin: 0;
    font-size: 1.35rem;
    font-weight: 700;
    letter-spacing: 0.01em;
}

#header-banner p {
    margin: 6px 0 0 0;
    color: #94a3b8;
    font-size: 0.9rem;
}

#app-shell .prose,
#app-shell .md,
#app-shell label,
#app-shell .gr-markdown,
#app-shell .gradio-markdown {
    color: #e2e8f0 !important;
}

#app-shell [data-testid="chatbot"] {
    background: #111827 !important;
    border-radius: 0 0 16px 16px;
}

#app-shell [data-testid="chatbot"] .message,
#app-shell .message,
#app-shell .bubble {
    border-radius: 14px !important;
    border: 1px solid #243041;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.18);
}

#app-shell textarea,
#app-shell input,
#app-shell .gr-textbox textarea {
    background: #0f172a !important;
    color: #e5e7eb !important;
    border: 1px solid #334155 !important;
}

#app-shell textarea:focus,
#app-shell input:focus,
#app-shell .gr-textbox textarea:focus {
    border: 1px solid #6366f1 !important;
    box-shadow: 0 0 0 1px #6366f1 !important;
}

#app-shell button {
    border-radius: 10px !important;
    border: 1px solid #334155 !important;
    background: #1e293b !important;
    color: #e2e8f0 !important;
}

#app-shell button:hover {
    background: #273449 !important;
}

#footer-note {
    text-align: center;
    color: #94a3b8;
    padding: 12px 10px 18px 10px;
    font-size: 0.88rem;
}
"""


def build_prompt(messages: list[dict]) -> str:
    """Convert chat messages into a ChatML-style prompt string.

    Args:
        messages: List of message dictionaries with role/content keys.

    Returns:
        A single formatted prompt string ending with assistant prefix.
    """
    prompt_parts = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        prompt_parts.append(f"<|im_start|>{role}\n{content}<|im_end|>\n")

    prompt_parts.append("<|im_start|>assistant\n")
    return "".join(prompt_parts)


def respond(
    message: str,
    history: list[dict],
    system_prompt: str,
    max_tokens: int,
    temperature: float,
    top_p: float,
) -> Generator[str, None, None]:
    """Generate and stream assistant responses for Gradio ChatInterface.

    Args:
        message: Current user message.
        history: Existing chat history in Gradio messages format.
        system_prompt: Editable system instruction from UI.
        max_tokens: Max new tokens to generate.
        temperature: Sampling temperature.
        top_p: Nucleus sampling value.

    Yields:
        Progressive response text chunks suitable for live UI streaming.
    """
    messages = [{"role": "system", "content": system_prompt}]

    # Preserve prior turns so the model responds with context continuity.
    for item in history or []:
        if isinstance(item, dict) and "role" in item and "content" in item:
            messages.append(item)
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            user_text, assistant_text = item
            messages.append({"role": "user", "content": str(user_text or "")})
            messages.append(
                {"role": "assistant", "content": str(assistant_text or "")}
            )

    messages.append({"role": "user", "content": message})

    candidate_model_ids = []
    if MODEL_ID:
        candidate_model_ids.append(MODEL_ID)
    candidate_model_ids.extend(
        [PRIMARY_MODEL_ID, *COMPATIBLE_FALLBACK_MODELS, FALLBACK_MODEL_ID]
    )

    # Remove duplicates while preserving order.
    deduped_model_ids = list(dict.fromkeys(candidate_model_ids))

    last_error = None
    for model_id in deduped_model_ids:
        try:
            temp_client = InferenceClient(model=model_id, token=HF_TOKEN)
            yield from stream_chat_reply(
                inference_client=temp_client,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
            )
            return
        except Exception as e:
            last_error = e

    error_text = str(last_error).strip() if last_error else "Unknown error"
    if not error_text:
        error_text = repr(last_error)
    yield f"Sorry, I encountered an error: {error_text}. Please try again."


with gr.Blocks(title="IntelliChat AI Assistant") as demo:
    with gr.Column(elem_id="app-shell"):
        gr.HTML(
            """
            <div id="header-banner">
                <h1>IntelliChat AI Assistant</h1>
                <p>Powered by Qwen2-7B • Free • Open Source</p>
            </div>
            """
        )

        system_prompt_box = gr.Textbox(
            label="System Prompt",
            lines=3,
            value=SYSTEM_PROMPT,
            render=False,
        )
        max_tokens_slider = gr.Slider(
            label="Max Tokens",
            minimum=64,
            maximum=2048,
            value=512,
            step=1,
            render=False,
        )
        temp_slider = gr.Slider(
            label="Temperature",
            minimum=0.1,
            maximum=2.0,
            value=0.7,
            step=0.1,
            render=False,
        )
        top_p_slider = gr.Slider(
            label="Top-P",
            minimum=0.1,
            maximum=1.0,
            value=0.9,
            step=0.05,
            render=False,
        )

        gr.ChatInterface(
            fn=respond,
            chatbot=gr.Chatbot(height=500),
            additional_inputs=[
                system_prompt_box,
                max_tokens_slider,
                temp_slider,
                top_p_slider,
            ],
        )

        gr.Markdown(
            "Built with Gradio and Hugging Face • IntelliChat v1.0",
            elem_id="footer-note",
        )

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft(), css=CUSTOM_CSS)
