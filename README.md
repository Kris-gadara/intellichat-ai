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

IntelliChat AI Assistant is a production-ready, open-source chatbot built with Gradio and powered by free Hugging Face Inference API models. It streams responses in real time, offers configurable generation settings, and deploys easily to Hugging Face Spaces at zero cost.

## ✨ Features

- Real-time token streaming with Hugging Face `InferenceClient`
- Primary model: `Qwen/Qwen2-7B-Instruct`
- Automatic fallback model: `microsoft/Phi-2` for resiliency
- Clean Gradio chat UI with advanced controls
- Editable system prompt for behavior tuning
- Zero-cost deployment on Hugging Face Spaces

## 🚀 Quick Deploy to HF Spaces

1. Go to https://huggingface.co/spaces and click **Create new Space**.
2. Set Space name to `intellichat-ai-assistant` and choose **Gradio** SDK.
3. Upload `app.py`, `requirements.txt`, `README.md`, and `.env.example`.
4. Open **Settings → Variables and Secrets**.
5. Add secret `HF_TOKEN` with your token from https://huggingface.co/settings/tokens.
6. Wait for the build to complete, then open and share your Space URL.

## 🔧 Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/Kris-gadara/intellichat-ai.git
   cd intellichat-ai
   ```
2. Create and activate a virtual environment (recommended).
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set your token:
   - Windows PowerShell:
     ```powershell
     $env:HF_TOKEN="your_huggingface_token"
     ```
   - macOS/Linux:
     ```bash
     export HF_TOKEN="your_huggingface_token"
     ```
5. Run the app:
   ```bash
   python app.py
   ```

## ⚙️ Configuration

| Variable      | Default                  | Description                                                   |
| ------------- | ------------------------ | ------------------------------------------------------------- |
| `HF_TOKEN`    | `""`                     | Hugging Face access token used for Inference API requests.    |
| `MODEL_ID`    | `Qwen/Qwen2-7B-Instruct` | Optional model override through environment (if implemented). |
| `max_tokens`  | `512`                    | Maximum generated tokens per response from the UI slider.     |
| `temperature` | `0.7`                    | Sampling creativity from the UI slider.                       |
| `top_p`       | `0.9`                    | Nucleus sampling parameter from the UI slider.                |

## 🛠️ Tech Stack

| Component      | Technology                                                     |
| -------------- | -------------------------------------------------------------- |
| Frontend/UI    | Gradio                                                         |
| Primary Model  | Qwen/Qwen2-7B-Instruct                                         |
| Fallback Model | microsoft/Phi-2                                                |
| Inference      | Hugging Face Inference API (`huggingface_hub.InferenceClient`) |
| Runtime        | Python 3.10+                                                   |
| Deployment     | Hugging Face Spaces (Gradio SDK)                               |

## 📝 License

MIT
