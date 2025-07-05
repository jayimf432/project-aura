"""
Image generation endpoints (Stable Diffusion text-to-image)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import numpy as np
from PIL import Image
import io
from fastapi.responses import StreamingResponse
from loguru import logger
import torch
from app.core.config import settings
from diffusers import StableDiffusionPipeline

router = APIRouter()

class TextToImageRequest(BaseModel):
    prompt: str
    negative_prompt: Optional[str] = None
    width: int = 512
    height: int = 512
    num_inference_steps: int = 30
    guidance_scale: float = 7.5
    seed: Optional[int] = None

@router.post("/generate", response_class=StreamingResponse)
async def generate_image(request: TextToImageRequest):
    """Generate an image from text using Stable Diffusion"""
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Loading Stable Diffusion pipeline on {device}")
        pipe = StableDiffusionPipeline.from_pretrained(
            settings.DIFFUSION_MODEL_ID,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32
        )
        pipe = pipe.to(device)
        if hasattr(pipe, "enable_xformers_memory_efficient_attention"):
            pipe.enable_xformers_memory_efficient_attention()
        generator = torch.Generator(device=device)
        if request.seed is not None:
            generator = generator.manual_seed(request.seed)
        logger.info(f"Generating image for prompt: {request.prompt}")
        with torch.no_grad():
            result = pipe(
                prompt=request.prompt,
                negative_prompt=request.negative_prompt,
                width=request.width,
                height=request.height,
                num_inference_steps=request.num_inference_steps,
                guidance_scale=request.guidance_scale,
                generator=generator
            )
        image: Image.Image = result.images[0]
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)
        return StreamingResponse(buf, media_type="image/png")
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate image") 