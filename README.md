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

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/project-aura.git
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