"""
Stable Video Diffusion service for video transformation
"""

import torch
import numpy as np
from typing import List, Optional, Tuple
from diffusers import StableVideoDiffusionPipeline
from diffusers.utils import export_to_video, load_image
from PIL import Image
import cv2
from loguru import logger
from app.core.config import settings


class SVDService:
    """Handles AI-powered video transformation using Stable Video Diffusion"""
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipeline = None
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize Stable Video Diffusion model"""
        try:
            logger.info(f"Initializing Stable Video Diffusion on {self.device}")
            
            # Load Stable Video Diffusion pipeline
            self.pipeline = StableVideoDiffusionPipeline.from_pretrained(
                settings.SVD_MODEL_ID,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                variant="fp16" if self.device == "cuda" else None,
            )
            
            # Move to device
            self.pipeline = self.pipeline.to(self.device)
            
            # Enable memory efficient attention if available
            if hasattr(self.pipeline, "enable_xformers_memory_efficient_attention"):
                self.pipeline.enable_xformers_memory_efficient_attention()
            
            logger.info("Stable Video Diffusion initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing Stable Video Diffusion: {e}")
            raise
    
    async def transform_video(
        self,
        frames: List[np.ndarray],
        prompt: str,
        conditions: List[str] = None,
        style_preset: Optional[str] = None,
        quality: str = "high",
        num_frames: int = 25,
        fps: int = 7
    ) -> List[np.ndarray]:
        """Transform video using Stable Video Diffusion"""
        
        if not frames:
            raise ValueError("No frames provided")
        
        try:
            logger.info(f"Starting video transformation with SVD for {len(frames)} input frames")
            
            # Build comprehensive prompt
            full_prompt = self._build_prompt(prompt, conditions, style_preset)
            
            # Set generation parameters based on quality
            generation_params = self._get_generation_params(quality, num_frames, fps)
            
            # Use first frame as conditioning image
            conditioning_frame = frames[0]
            pil_image = Image.fromarray(conditioning_frame)
            
            # Generate video using SVD
            logger.info("Generating video with Stable Video Diffusion...")
            with torch.no_grad():
                video_frames = self.pipeline(
                    prompt=full_prompt,
                    image=pil_image,
                    **generation_params
                ).frames[0]
            
            # Convert video frames to numpy arrays
            transformed_frames = []
            for frame in video_frames:
                # Convert PIL to numpy
                frame_np = np.array(frame)
                transformed_frames.append(frame_np)
            
            logger.info(f"Video transformation completed: {len(transformed_frames)} frames generated")
            return transformed_frames
            
        except Exception as e:
            logger.error(f"Error in video transformation: {e}")
            raise
    
    async def transform_video_with_control(
        self,
        frames: List[np.ndarray],
        prompt: str,
        conditions: List[str] = None,
        style_preset: Optional[str] = None,
        quality: str = "high",
        num_frames: int = 25,
        fps: int = 7,
        motion_bucket_id: int = 127,
        noise_aug_strength: float = 0.1
    ) -> List[np.ndarray]:
        """Transform video using SVD with motion control"""
        
        if not frames:
            raise ValueError("No frames provided")
        
        try:
            logger.info(f"Starting controlled video transformation with SVD")
            
            # Build comprehensive prompt
            full_prompt = self._build_prompt(prompt, conditions, style_preset)
            
            # Set generation parameters with motion control
            generation_params = self._get_generation_params_with_control(
                quality, num_frames, fps, motion_bucket_id, noise_aug_strength
            )
            
            # Use first frame as conditioning image
            conditioning_frame = frames[0]
            pil_image = Image.fromarray(conditioning_frame)
            
            # Generate video using SVD with motion control
            logger.info("Generating video with motion control...")
            with torch.no_grad():
                video_frames = self.pipeline(
                    prompt=full_prompt,
                    image=pil_image,
                    **generation_params
                ).frames[0]
            
            # Convert video frames to numpy arrays
            transformed_frames = []
            for frame in video_frames:
                frame_np = np.array(frame)
                transformed_frames.append(frame_np)
            
            logger.info(f"Controlled video transformation completed: {len(transformed_frames)} frames")
            return transformed_frames
            
        except Exception as e:
            logger.error(f"Error in controlled video transformation: {e}")
            raise
    
    def _build_prompt(
        self,
        base_prompt: str,
        conditions: List[str] = None,
        style_preset: Optional[str] = None
    ) -> str:
        """Build comprehensive prompt from components"""
        
        prompt_parts = [base_prompt]
        
        # Add conditions
        if conditions:
            prompt_parts.extend(conditions)
        
        # Add style preset
        if style_preset:
            style_modifiers = {
                "cinematic": "cinematic lighting, professional film look, dramatic atmosphere",
                "vintage": "vintage film look, warm tones, film grain, retro aesthetic",
                "futuristic": "futuristic, neon lights, cyberpunk, sci-fi aesthetic",
                "natural": "natural lighting, clean colors, balanced exposure",
                "artistic": "artistic interpretation, creative styling, unique visual approach"
            }
            
            if style_preset in style_modifiers:
                prompt_parts.append(style_modifiers[style_preset])
        
        # Add video-specific quality modifiers
        prompt_parts.extend([
            "high quality video",
            "smooth motion",
            "temporal consistency",
            "professional cinematography",
            "stable camera movement"
        ])
        
        # Combine all parts
        full_prompt = ", ".join(prompt_parts)
        
        logger.info(f"Built SVD prompt: {full_prompt}")
        return full_prompt
    
    def _get_generation_params(self, quality: str, num_frames: int, fps: int) -> dict:
        """Get generation parameters based on quality setting"""
        
        base_params = {
            "num_inference_steps": 25,
            "guidance_scale": 9.0,
            "negative_prompt": "blurry, low quality, distorted, artifacts, flickering, inconsistent lighting, temporal artifacts, poor video quality",
            "num_frames": num_frames,
            "fps": fps,
            "motion_bucket_id": 127,
            "noise_aug_strength": 0.1
        }
        
        quality_params = {
            "low": {
                "num_inference_steps": 20,
                "guidance_scale": 7.5,
                "num_frames": min(num_frames, 14),
                "fps": min(fps, 6)
            },
            "medium": {
                "num_inference_steps": 25,
                "guidance_scale": 9.0,
                "num_frames": num_frames,
                "fps": fps
            },
            "high": {
                "num_inference_steps": 50,
                "guidance_scale": 12.5,
                "num_frames": num_frames,
                "fps": fps
            }
        }
        
        if quality in quality_params:
            base_params.update(quality_params[quality])
        
        return base_params
    
    def _get_generation_params_with_control(
        self, 
        quality: str, 
        num_frames: int, 
        fps: int, 
        motion_bucket_id: int, 
        noise_aug_strength: float
    ) -> dict:
        """Get generation parameters with motion control"""
        
        base_params = self._get_generation_params(quality, num_frames, fps)
        base_params.update({
            "motion_bucket_id": motion_bucket_id,
            "noise_aug_strength": noise_aug_strength
        })
        
        return base_params
    
    async def test_model(self) -> bool:
        """Test if the SVD model is working correctly"""
        try:
            logger.info("Testing Stable Video Diffusion model...")
            
            # Create a simple test image
            test_image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
            pil_image = Image.fromarray(test_image)
            
            # Test generation with minimal parameters
            with torch.no_grad():
                result = self.pipeline(
                    prompt="test video",
                    image=pil_image,
                    num_inference_steps=5,
                    num_frames=8,
                    fps=7
                )
            
            if result.frames and len(result.frames[0]) > 0:
                logger.info("SVD model test successful")
                return True
            else:
                logger.error("SVD model test failed - no frames generated")
                return False
                
        except Exception as e:
            logger.error(f"SVD model test failed: {e}")
            return False
    
    def get_motion_presets(self) -> dict:
        """Get available motion presets for video generation"""
        return {
            "static": {
                "motion_bucket_id": 1,
                "description": "Very little motion, static scenes"
            },
            "subtle": {
                "motion_bucket_id": 32,
                "description": "Subtle motion, gentle camera movements"
            },
            "normal": {
                "motion_bucket_id": 127,
                "description": "Normal motion, typical video movement"
            },
            "dynamic": {
                "motion_bucket_id": 255,
                "description": "Dynamic motion, fast camera movements"
            },
            "extreme": {
                "motion_bucket_id": 511,
                "description": "Extreme motion, very fast movements"
            }
        }
    
    def get_quality_presets(self) -> dict:
        """Get available quality presets"""
        return {
            "fast": {
                "num_inference_steps": 20,
                "guidance_scale": 7.5,
                "description": "Fast generation, lower quality"
            },
            "balanced": {
                "num_inference_steps": 25,
                "guidance_scale": 9.0,
                "description": "Balanced speed and quality"
            },
            "high": {
                "num_inference_steps": 50,
                "guidance_scale": 12.5,
                "description": "High quality, slower generation"
            }
        } 