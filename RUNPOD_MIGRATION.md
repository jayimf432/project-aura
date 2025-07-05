# Project Aura: Vast AI to RunPod Migration Guide

## Overview

This guide helps you migrate your Project Aura deployment from Vast AI to RunPod. The main differences are in environment setup, port configuration, and networking.

## Key Differences

| Aspect | Vast AI | RunPod |
|--------|---------|--------|
| **Port Configuration** | Uses external IP addresses | Uses localhost with port forwarding |
| **Environment** | Development mode | Production mode |
| **Networking** | Direct external access | Port-forwarded access |
| **Setup** | Manual installation | Automated setup script |

## Migration Steps

### 1. Create RunPod Instance

1. Go to [RunPod.io](https://runpod.io)
2. Create a new pod with:
   - **GPU**: RTX 4090, A100, or similar (CUDA 12.x)
   - **OS**: Ubuntu 22.04 or PyTorch base image
   - **Memory**: 16GB+ RAM recommended
   - **Storage**: 50GB+ recommended

### 2. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/jayimf432/project-aura.git
cd project-aura

# Run the RunPod setup script
./setup-runpod.sh
```

### 3. Verify Setup

```bash
# Test the setup
./test-runpod.sh
```

### 4. Start the Application

```bash
# Start both services
./start-runpod.sh

# Or start individually
./start-backend-runpod.sh  # Backend only
./start-frontend-runpod.sh # Frontend only
```

## Environment Variables

RunPod uses these environment variables:

```bash
# Backend port (default: 8000)
export RUNPOD_PORT=8000

# Frontend port (default: 5173)
export FRONTEND_PORT=5173
```

## Port Configuration

### RunPod Port Forwarding

1. **Backend API**: Configure port 8000 in RunPod
2. **Frontend**: Configure port 5173 in RunPod
3. **Access URLs**:
   - Frontend: `http://localhost:5173`
   - Backend: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`

### Vast AI vs RunPod URLs

| Service | Vast AI | RunPod |
|---------|---------|--------|
| Frontend | `http://YOUR_IP:5173` | `http://localhost:5173` |
| Backend | `http://YOUR_IP:8000` | `http://localhost:8000` |
| API Docs | `http://YOUR_IP:8000/docs` | `http://localhost:8000/docs` |

## Configuration Changes

### Backend Configuration

The RunPod setup automatically creates:
- Production environment settings
- Proper CORS configuration for localhost
- Optimized for RunPod networking

### Frontend Configuration

The frontend is configured to:
- Connect to localhost backend
- Use RunPod port configuration
- Work with RunPod's networking setup

## Troubleshooting

### Common Issues

1. **Port Not Accessible**
   ```bash
   # Check if ports are configured in RunPod
   # Ensure port forwarding is set up correctly
   ```

2. **GPU Not Detected**
   ```bash
   # Check GPU availability
   nvidia-smi
   
   # The setup will automatically use CPU if no GPU is found
   ```

3. **Dependencies Not Installed**
   ```bash
   # Re-run the setup script
   ./setup-runpod.sh
   ```

4. **Permission Issues**
   ```bash
   # Make scripts executable
   chmod +x setup-runpod.sh start-runpod.sh test-runpod.sh
   ```

### Performance Optimization

1. **GPU Memory**: Monitor GPU memory usage with `nvidia-smi`
2. **CPU Usage**: Check CPU usage with `htop`
3. **Memory**: Monitor RAM usage with `free -h`

## Migration Checklist

- [ ] RunPod instance created with appropriate GPU
- [ ] Repository cloned
- [ ] `./setup-runpod.sh` executed successfully
- [ ] `./test-runpod.sh` shows all tests passing
- [ ] Application starts with `./start-runpod.sh`
- [ ] Frontend accessible at `http://localhost:5173`
- [ ] Backend API accessible at `http://localhost:8000`
- [ ] API documentation accessible at `http://localhost:8000/docs`
- [ ] Video upload and processing working
- [ ] AI transformations functioning correctly

## Support

If you encounter issues during migration:

1. Check the troubleshooting section above
2. Review the main README.md for detailed setup instructions
3. Ensure all system requirements are met
4. Verify RunPod instance configuration

## Benefits of RunPod Migration

- **Simplified Setup**: Automated installation script
- **Better Performance**: Optimized for RunPod's infrastructure
- **Production Ready**: Proper environment configuration
- **Easier Management**: Dedicated scripts for RunPod environment
- **Cost Effective**: Often more cost-effective than Vast AI 