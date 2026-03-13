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

HF_TOKEN = os.environ.get("HF_TOKEN", "")
client = InferenceClient(model="Qwen/Qwen2-7B-Instruct", token=HF_TOKEN)
fallback_client = InferenceClient(model=FALLBACK_MODEL_ID, token=HF_TOKEN)

# Optional override for the primary model, e.g., MODEL_ID=microsoft/Phi-2.
MODEL_ID = os.environ.get("MODEL_ID", "").strip()
if MODEL_ID:
    client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)


CUSTOM_CSS = """
#app-shell {
    max-width: 1100px;
    margin: 24px auto;
    border-radius: 18px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.10);
    overflow: hidden;
    background: #ffffff;
}

#header-banner {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #ffffff;
    padding: 24px 28px;
}

#header-banner h1 {
    margin: 0;
    font-size: 1.9rem;
    font-weight: 700;
}

#header-banner p {
    margin: 8px 0 0 0;
    font-size: 1rem;
    opacity: 0.95;
}

#footer-note {
    text-align: center;
    color: #4b5563;
    padding: 14px 10px 22px 10px;
    font-size: 0.92rem;
}

/* Rounded chat bubbles */
#app-shell .message,
#app-shell .bubble,
#app-shell [data-testid="chatbot"] .message {
    border-radius: 14px !important;
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

    messages.append({"role": "user", "content": message})
    prompt = build_prompt(messages)

    try:
        stream = client.text_generation(
            prompt,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stream=True,
            stop_sequences=["<|im_end|>", "<|im_start|>"],
        )
        response = ""
        for token in stream:
            response += token
            yield response
    except Exception:
        # Primary model failed; try the lightweight fallback for resilience.
        try:
            stream = fallback_client.text_generation(
                prompt,
                max_new_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                stream=True,
                stop_sequences=["<|im_end|>", "<|im_start|>"],
            )
            response = ""
            for token in stream:
                response += token
                yield response
        except Exception as e:
            yield f"⚠️ Sorry, I encountered an error: {str(e)}. Please try again."


with gr.Blocks(
    theme=gr.themes.Soft(),
    css=CUSTOM_CSS,
    title="IntelliChat AI Assistant",
) as demo:
    with gr.Column(elem_id="app-shell"):
        gr.HTML(
            """
            <div id="header-banner">
                <h1>🤖 IntelliChat AI Assistant</h1>
                <p>Powered by Qwen2-7B • Free • Open Source</p>
            </div>
            """
        )

        gr.Markdown("Powered by Qwen2-7B • Free • Open Source")

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
            type="messages",
            chatbot=gr.Chatbot(type="messages", height=500),
            additional_inputs=[
                system_prompt_box,
                max_tokens_slider,
                temp_slider,
                top_p_slider,
            ],
            additional_inputs_accordion_name="▼ Advanced Settings",
            submit_btn="Send 🚀",
            clear_btn="Clear Chat 🗑️",
        )

        gr.Markdown(
            "Built with ❤️ using Gradio + Hugging Face • IntelliChat v1.0",
            elem_id="footer-note",
        )

if __name__ == "__main__":
    demo.launch(show_api=False)
