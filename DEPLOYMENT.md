# 🚀 Aureeq Deployment Guide

This project is fully Dockerized for easy deployment to any VPS (e.g., Hostinger, AWS, DigitalOcean).

## 📋 Prerequisites
- Docker & Docker Compose installed on the VPS.
- A functional domain or public IP.

## 🚀 Quick Start (Production)

1.  **Transfer Files**: Copy the project files to your VPS.
2.  **Configure Environment**: 
    - Rename `.env.example` to `.env`.
    - Set `BACKEND_API_URL` to your public endpoint (e.g., `https://aureeqapi.site.com`).
3.  **Launch Services**:
    ```bash
    docker-compose up -d --build
    ```
4.  **Verify**:
    - Frontend will be accessible on port **12080**.
    - Backend API on port **8001**.
    - TTS Engine on port **8880**.

## 🔧 Environment Variables (.env)
| Variable | Description | Default |
| :--- | :--- | :--- |
| `BACKEND_API_URL` | The public URL of your backend (Vite bakes this into the build) | `https://aureeqapi.kamsoft.tech` |
| `MODEL_LLAMA` | The Llama model to use in Ollama | `llama3.1:8b` |
| `TTS_VOICE` | The Kokoro UK Male voice | `bm_george` |
| `OLLAMA_HOST` | Internal/External address for Ollama | `http://aureeq-ai:11434` |

## 🛠 Troubleshooting
- **Port Conflict**: If port **12080** is taken, change the mapping in `docker-compose.yml`.
- **Memory Issues**: If the VPS has less than 8GB RAM, ensure you have a **swap file** (at least 4GB) to handle Llama 3.1 8B.
- **Logs**: View logs with `docker-compose logs -f aureeq-backend`.

## 📦 Maintenance
- **Menu Sync**: The backend automatically syncs with your WordPress store every 24 hours.
- **Development Tools**: All testing and verification scripts are located in the `tools/` directory. These are excluded from the main Docker build.
