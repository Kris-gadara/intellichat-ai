---
title: IntelliChat AI Assistant
emoji: 🤖
colorFrom: purple
colorTo: blue
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
short_description: Free AI chatbot powered by Qwen2-7B on Hugging Face
---

# 🤖 IntelliChat AI Assistant

IntelliChat AI Assistant is a production-ready, zero-cost chatbot that runs on Hugging Face Spaces using free Hugging Face Inference API models. It provides live token streaming, ChatGPT-like conversational UX, customizable model controls, and resilient fallback inference for reliable responses.

## ✨ Features

- Real-time token streaming in the UI for fast perceived response time.
- Primary model: `Qwen/Qwen2-7B-Instruct` (free and strong instruction-following).
- Fallback model: `microsoft/Phi-2` if primary inference fails.
- ChatGPT-style interface with IntelliChat branding.
- Advanced controls for `system prompt`, `max tokens`, `temperature`, and `top_p`.
- Safe error handling with user-friendly messages.
- One-click deployment to Hugging Face Spaces.

## 🏗️ Architecture

```text
User Message
   ↓
Gradio ChatInterface
   ↓
respond(message, history, ...)
   ↓
build_prompt() -> ChatML-style prompt
   ↓
InferenceClient.text_generation(stream=True)
   ↓
Token-by-token yield
   ↓
Live streamed response in UI
```

## 📂 Project Structure

```text
.
├── app.py
├── requirements.txt
├── README.md
└── .env.example
```

## 🚀 Quick Deploy to HF Spaces

1. Go to https://huggingface.co/spaces and click **Create new Space**.
2. Use Space name: `intellichat-ai-assistant`.
3. Select **SDK: Gradio**.
4. Upload these files: `app.py`, `requirements.txt`, `README.md`, `.env.example`.
5. Open **Settings → Variables and Secrets**.
6. Add secret:
   - **Name**: `HF_TOKEN`
   - **Value**: your token from https://huggingface.co/settings/tokens
7. Wait for build + launch, then share your live Space URL.

## 🔧 Local Development

### Prerequisites

- Python 3.10+
- A free Hugging Face account
- Hugging Face token with inference access

### Setup

```bash
git clone https://github.com/Kris-gadara/intellichat-ai.git
cd intellichat-ai
python -m venv .venv
```

#### Activate virtual environment

- **Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

- **macOS/Linux**

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Set environment variables

- **Windows PowerShell**

```powershell
$env:HF_TOKEN="your_huggingface_token"
```

- **macOS/Linux**

```bash
export HF_TOKEN="your_huggingface_token"
```

Optional model override:

```bash
export MODEL_ID="microsoft/Phi-2"
```

### Run the app

```bash
python app.py
```

Then open the local URL shown in terminal (usually `http://127.0.0.1:7860`).

## ⚙️ Configuration

| Variable      | Default | Description                                                                 |
| ------------- | ------- | --------------------------------------------------------------------------- |
| `HF_TOKEN`    | `""`    | Hugging Face token used by `InferenceClient` for API calls.                 |
| `MODEL_ID`    | unset   | Optional override for primary model (defaults to `Qwen/Qwen2-7B-Instruct`). |
| `max_tokens`  | `512`   | Maximum number of new tokens generated per reply.                           |
| `temperature` | `0.7`   | Sampling creativity (higher is more diverse).                               |
| `top_p`       | `0.9`   | Nucleus sampling threshold.                                                 |

## 🛠️ Tech Stack

| Component      | Technology                        |
| -------------- | --------------------------------- |
| Frontend/UI    | Gradio                            |
| Primary Model  | `Qwen/Qwen2-7B-Instruct`          |
| Fallback Model | `microsoft/Phi-2`                 |
| Inference      | `huggingface_hub.InferenceClient` |
| Deployment     | Hugging Face Spaces (Gradio SDK)  |
| Language       | Python 3.10+                      |

## ✅ Production Notes

- Keep `HF_TOKEN` in Hugging Face Space Secrets (never commit real tokens).
- Use fallback model to improve availability during high load.
- Keep prompts concise to reduce latency and token usage.
- Adjust `max_tokens` to control cost/performance behavior.

## 🧪 Troubleshooting

- **Authentication error**: verify `HF_TOKEN` is valid and set in env/secrets.
- **Slow responses**: reduce `max_tokens` and temperature; fallback to `microsoft/Phi-2`.
- **Build issues on Space**: confirm `sdk_version`, `app_file`, and dependency install logs.
- **Empty output**: check model availability and inference API status.

## 🔐 Security

- Do not hardcode API tokens in source files.
- Do not commit `.env` files containing secrets.
- Rotate tokens if exposed.

## 📝 License

MIT
