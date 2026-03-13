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

# IntelliChat AI Assistant

IntelliChat AI Assistant is a production-ready chatbot built with Gradio and powered by free Hugging Face Inference API models. It delivers live streaming responses, a polished dark interface, and robust model failover to keep responses available when one model is temporarily unsupported.

## Live Demo UI

![IntelliChat Live Demo](Screenshot%202026-03-13%20184532.png)

## Features

- Real-time token streaming in the chat window.
- Premium dark UI inspired by modern AI chat products.
- Primary model with automatic fallback model routing.
- Advanced generation controls for prompt and sampling.
- Error-safe backend with friendly fallback messages.
- Zero-cost deployment on Hugging Face Spaces.

## Architecture

```text
User Message
   ↓
Gradio ChatInterface
   ↓
respond(message, history, system_prompt, max_tokens, temperature, top_p)
   ↓
Build messages list (system + history + user)
   ↓
InferenceClient.chat.completions.create(stream=True)
   ↓
Token chunks streamed to Gradio UI
```

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── README.md
├── .env.example
└── Screenshot 2026-03-13 184532.png
```

## Quick Deploy to Hugging Face Spaces

1. Go to https://huggingface.co/spaces and click **Create new Space**.
2. Set Space name to `intellichat-ai-assistant`.
3. Choose **SDK: Gradio**.
4. Upload: `app.py`, `requirements.txt`, `README.md`, `.env.example`, and screenshot file (optional).
5. Open **Settings → Variables and Secrets**.
6. Add secret:
   - Name: `HF_TOKEN`
   - Value: your token from https://huggingface.co/settings/tokens
7. Wait for the build to finish and open your live Space URL.

## Local Development

### Prerequisites

- Python 3.10+
- Hugging Face account and API token

### Setup

```bash
git clone https://github.com/Kris-gadara/intellichat-ai.git
cd intellichat-ai
python -m venv .venv
```

### Activate venv

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Set environment variables

Windows PowerShell:

```powershell
$env:HF_TOKEN="your_huggingface_token"
```

macOS/Linux:

```bash
export HF_TOKEN="your_huggingface_token"
```

Optional model override:

```bash
export MODEL_ID="Qwen/Qwen2.5-7B-Instruct"
```

### Run

```bash
python app.py
```

Then open the local URL shown in terminal (commonly `http://127.0.0.1:7860`).

## Configuration

| Variable      | Default | Description                                     |
| ------------- | ------- | ----------------------------------------------- |
| `HF_TOKEN`    | `""`    | Hugging Face token used for inference requests. |
| `MODEL_ID`    | unset   | Optional manual model override.                 |
| `max_tokens`  | `512`   | Max output tokens per response.                 |
| `temperature` | `0.7`   | Response creativity control.                    |
| `top_p`       | `0.9`   | Nucleus sampling threshold.                     |

## Model Strategy

- Primary target: `Qwen/Qwen2-7B-Instruct`
- Compatibility fallbacks: `Qwen/Qwen2.5-7B-Instruct`, `meta-llama/Llama-3.1-8B-Instruct`
- Legacy fallback: `microsoft/Phi-2`

The app automatically tries models in order and streams from the first working provider/model pair.

## Tech Stack

| Component        | Technology                        |
| ---------------- | --------------------------------- |
| UI               | Gradio                            |
| Inference Client | `huggingface_hub.InferenceClient` |
| Runtime          | Python 3.10+                      |
| Deployment       | Hugging Face Spaces               |

## Troubleshooting

- **No response**: verify `HF_TOKEN` is valid and has inference access.
- **Model not supported**: set `MODEL_ID` to a supported model for your account.
- **Slow generation**: reduce `max_tokens`, set lower `temperature`.
- **Space build failure**: check build logs for dependency/install errors.

## Security Best Practices

- Keep secrets only in Hugging Face Space Secrets or local environment.
- Never commit real tokens into source control.
- Rotate tokens if accidentally exposed.

## License

MIT
