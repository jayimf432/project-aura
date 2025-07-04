# Project Aura 🌟

> **AI-Powered Cinematic Video Transformation**

Transform the atmosphere of any video—adjusting time of day, weather, and seasons—through an intelligent AI Creative Director.

## 🎯 Mission & Vision

To empower creators with an AI-native tool for cinematic control over video. Aura allows users to transform the atmosphere of any video through a simple, intuitive interface, guided by an intelligent AI Creative Director.

## ✨ Core Features

- **Video-to-Video Translation:** Upload a source video as the structural base for transformation
- **Multi-Condition Control:** Guide transformations with text prompts combining multiple conditions
- **AI Creative Director:** Conversational LLM agent for brainstorming and refining prompts
- **High-Fidelity Output:** Preserve motion and structure while maintaining temporal consistency
- **Modern Web Interface:** Clean, responsive, and user-friendly web application

## 🛠 Technology Stack

### Backend & AI Core
- **Python** with **FastAPI** - High-performance asynchronous backend
- **PyTorch** - Deep learning framework
- **Hugging Face** (`diffusers` & `transformers`) - State-of-the-art AI models
- **ControlNet** - Structural consistency guidance
- **OpenCV** - Video I/O and frame manipulation

### Frontend
- **React** with **TypeScript** - Modern, type-safe UI development
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework

### Deployment
- **Docker & Docker Compose** - Containerized services
- **Cloud Platform** - Scalable deployment

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Docker (optional, for containerized deployment)

### Development Setup

#### Option 1: Local Development (Mac/Windows/Linux)

1. **Clone the repository**
   ```bash
   git clone https://github.com/jayimf432/project-aura.git
   cd project-aura
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the Application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

#### Option 2: Vast.ai GPU Server Setup (Recommended for AI Processing)

1. **Create Vast.ai Instance**
   - Choose GPU: RTX 4090 or similar (CUDA 12.x)
   - OS: Ubuntu 22.04
   - SSH into your instance

2. **Clone and Setup**
   ```bash
   git clone https://github.com/jayimf432/project-aura.git
   cd project-aura
   ```

3. **Install PyTorch with CUDA**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Install System Dependencies**
   ```bash
   apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1
   ```

6. **Start Both Services**
   ```bash
   cd /root/project-aura
   ./start-dev.sh
   ```

7. **Access Your Application**
   - Get your server IP: `curl ifconfig.me`
   - Frontend: `http://YOUR_SERVER_IP:5173`
   - Backend API: `http://YOUR_SERVER_IP:8000`
   - API Docs: `http://YOUR_SERVER_IP:8000/docs`

### Environment Variables

Create `.env` files in both `backend/` and `frontend/` directories:

**Backend (.env):**
```env
ENVIRONMENT=development
DEBUG=true
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
HUGGINGFACE_API_KEY=your_token_here
```

**Frontend (.env):**
```env
VITE_API_URL=http://localhost:8000
```

## 📁 Project Structure

```
project-aura/
├── frontend/                 # React + TypeScript frontend
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── utils/          # Utility functions
│   │   ├── types/          # TypeScript type definitions
│   │   └── assets/         # Static assets
│   └── public/             # Public assets
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints and middleware
│   │   ├── core/           # Core configuration and security
│   │   ├── models/         # Data models
│   │   └── services/       # Business logic services
│   ├── models/             # AI model definitions
│   ├── services/           # External service integrations
│   ├── utils/              # Utility functions
│   └── tests/              # Test suite
└── docs/                   # Documentation
```

## 🔧 Recent Updates & Troubleshooting

### Platform Migration (Mac M1/M2 → Vast.ai Linux/CUDA)
- ✅ **PyTorch**: Updated from Apple Silicon (MPS) to CUDA 12.1
- ✅ **Dependencies**: Fixed version conflicts between `diffusers`, `transformers`, and `huggingface_hub`
- ✅ **System Dependencies**: Added OpenCV and other Linux-specific requirements
- ✅ **Configuration**: Fixed CORS_ORIGINS parsing for environment variables

### Common Issues & Solutions

**1. OpenCV Import Error:**
```bash
ImportError: libGL.so.1: cannot open shared object file
```
**Solution:**
```bash
apt-get install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1
```

**2. HuggingFace Hub Import Error:**
```bash
ImportError: cannot import name 'cached_download' from 'huggingface_hub'
```
**Solution:**
```bash
pip install --upgrade huggingface_hub diffusers transformers
```

**3. CORS Configuration Error:**
```bash
pydantic_settings.sources.SettingsError: error parsing value for field "CORS_ORIGINS"
```
**Solution:** Update `backend/app/core/config.py` with proper field validator (already fixed)

**4. PyTorch CUDA Installation:**
```bash
# For CUDA 12.x systems
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with cutting-edge AI technologies from Hugging Face
- Inspired by the creative potential of video transformation
- Powered by the open-source community

---

**Project Aura** - Where creativity meets AI-powered cinematic magic ✨ 