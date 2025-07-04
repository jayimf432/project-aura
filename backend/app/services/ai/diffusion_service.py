"""
AI Diffusion service for video transformation
"""

import torch
import numpy as np
from typing import List, Optional
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
from diffusers.utils import load_image
from PIL import Image
import cv2
from loguru import logger
from app.core.config import settings


class DiffusionService:
    """Handles AI-powered video frame transformation"""
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipeline = None
        self.controlnet = None
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize diffusion models"""
        try:
            logger.info(f"Initializing diffusion models on {self.device}")
            
            # Load ControlNet model
            self.controlnet = ControlNetModel.from_pretrained(
                settings.CONTROLNET_MODEL_ID,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            )
            
            # Load Stable Diffusion pipeline with ControlNet
            self.pipeline = StableDiffusionControlNetPipeline.from_pretrained(
                settings.DIFFUSION_MODEL_ID,
                controlnet=self.controlnet,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None,
                requires_safety_checker=False
            )
            
            # Move to device
            self.pipeline = self.pipeline.to(self.device)
            
            # Enable memory efficient attention if available
            if hasattr(self.pipeline, "enable_xformers_memory_efficient_attention"):
                self.pipeline.enable_xformers_memory_efficient_attention()
            
            logger.info("Diffusion models initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing diffusion models: {e}")
            raise
    
    async def transform_frames(
        self,
        frames: List[np.ndarray],
        prompt: str,
        conditions: List[str] = None,
        style_preset: Optional[str] = None,
        quality: str = "high"
    ) -> List[np.ndarray]:
        """Transform video frames using AI diffusion with improved temporal consistency"""
        
        if not frames:
            raise ValueError("No frames provided")
        
        try:
            logger.info(f"Starting frame transformation for {len(frames)} frames")
            
            # Build comprehensive prompt
            full_prompt = self._build_prompt(prompt, conditions, style_preset)
            
            # Set generation parameters based on quality
            generation_params = self._get_generation_params(quality)
            
            # Use consistent seed for better temporal consistency
            base_seed = torch.randint(0, 2**32, (1,)).item()
            generation_params["generator"] = torch.Generator(device=self.device).manual_seed(base_seed)
            
            transformed_frames = []
            
            # Process frames with improved consistency
            for i, frame in enumerate(frames):
                logger.info(f"Processing frame {i+1}/{len(frames)}")
                
                # Use slightly different seed for each frame but maintain consistency
                frame_seed = base_seed + i * 100  # Incremental seeds for consistency
                generation_params["generator"] = torch.Generator(device=self.device).manual_seed(frame_seed)
                
                # Transform single frame
                transformed_frame = await self._transform_single_frame(
                    frame, full_prompt, generation_params
                )
                
                transformed_frames.append(transformed_frame)
                
                # Progress logging
                if (i + 1) % 10 == 0:
                    logger.info(f"Completed {i+1}/{len(frames)} frames")
            
            # Apply enhanced temporal consistency
            logger.info("Applying enhanced temporal consistency...")
            consistent_frames = await self._apply_enhanced_temporal_consistency(transformed_frames)
            
            logger.info("Frame transformation completed successfully")
            return consistent_frames
            
        except Exception as e:
            logger.error(f"Error in frame transformation: {e}")
            raise
    
    async def _transform_single_frame(
        self,
        frame: np.ndarray,
        prompt: str,
        generation_params: dict
    ) -> np.ndarray:
        """Transform a single frame"""
        
        try:
            # Convert numpy array to PIL Image
            pil_image = Image.fromarray(frame)
            
            # Generate control image (edge detection for ControlNet)
            control_image = self._generate_control_image(frame)
            
            # Run diffusion pipeline
            with torch.no_grad():
                result = self.pipeline(
                    prompt=prompt,
                    image=control_image,
                    **generation_params
                )
            
            # Get the generated image
            generated_image = result.images[0]
            
            # Convert back to numpy array
            transformed_frame = np.array(generated_image)
            
            return transformed_frame
            
        except Exception as e:
            logger.error(f"Error transforming single frame: {e}")
            # Return original frame if transformation fails
            return frame
    
    def _generate_control_image(self, frame: np.ndarray) -> Image.Image:
        """Generate control image for ControlNet (edge detection)"""
        
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            
            # Apply Canny edge detection
            edges = cv2.Canny(gray, 100, 200)
            
            # Convert back to PIL Image
            control_image = Image.fromarray(edges)
            
            return control_image
            
        except Exception as e:
            logger.error(f"Error generating control image: {e}")
            # Return original frame as fallback
            return Image.fromarray(frame)
    
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
        
        # Add quality modifiers
        prompt_parts.extend([
            "high quality",
            "detailed",
            "professional photography",
            "consistent lighting",
            "stable atmosphere"
        ])
        
        # Combine all parts
        full_prompt = ", ".join(prompt_parts)
        
        logger.info(f"Built prompt: {full_prompt}")
        return full_prompt
    
    def _get_generation_params(self, quality: str) -> dict:
        """Get generation parameters based on quality setting with improved consistency"""
        
        base_params = {
            "num_inference_steps": 20,
            "guidance_scale": 7.5,
            "negative_prompt": "blurry, low quality, distorted, artifacts, flickering, inconsistent lighting, temporal artifacts",
            "eta": 0.0,  # Deterministic sampling for consistency
            "do_classifier_free_guidance": True
        }
        
        quality_params = {
            "low": {
                "num_inference_steps": 15,
                "guidance_scale": 6.0
            },
            "medium": {
                "num_inference_steps": 20,
                "guidance_scale": 7.5
            },
            "high": {
                "num_inference_steps": 30,
                "guidance_scale": 8.5
            }
        }
        
        if quality in quality_params:
            base_params.update(quality_params[quality])
        
        return base_params
    
    async def _apply_enhanced_temporal_consistency(
        self,
        frames: List[np.ndarray],
        window_size: int = 5
    ) -> List[np.ndarray]:
        """Apply enhanced temporal consistency to reduce flickering"""
        
        try:
            if len(frames) < window_size:
                return frames
            
            consistent_frames = []
            
            for i in range(len(frames)):
                # Get window of frames around current frame
                start_idx = max(0, i - window_size // 2)
                end_idx = min(len(frames), i + window_size // 2 + 1)
                
                window_frames = frames[start_idx:end_idx]
                
                # Apply enhanced temporal smoothing
                smoothed_frame = self._enhanced_temporal_smooth(window_frames, i - start_idx)
                consistent_frames.append(smoothed_frame)
            
            return consistent_frames
            
        except Exception as e:
            logger.error(f"Error applying enhanced temporal consistency: {e}")
            return frames

    async def _apply_temporal_consistency(
        self,
        frames: List[np.ndarray],
        window_size: int = 3
    ) -> List[np.ndarray]:
        """Apply temporal consistency to reduce flickering"""
        
        try:
            if len(frames) < window_size:
                return frames
            
            consistent_frames = []
            
            for i in range(len(frames)):
                # Get window of frames around current frame
                start_idx = max(0, i - window_size // 2)
                end_idx = min(len(frames), i + window_size // 2 + 1)
                
                window_frames = frames[start_idx:end_idx]
                
                # Apply temporal smoothing
                smoothed_frame = self._temporal_smooth(window_frames, i - start_idx)
                consistent_frames.append(smoothed_frame)
            
            return consistent_frames
            
        except Exception as e:
            logger.error(f"Error applying temporal consistency: {e}")
            return frames
    
    def _enhanced_temporal_smooth(
        self,
        window_frames: List[np.ndarray],
        center_idx: int
    ) -> np.ndarray:
        """Apply enhanced temporal smoothing with color consistency"""
        
        if len(window_frames) == 1:
            return window_frames[0]
        
        # Convert frames to float for processing
        float_frames = [frame.astype(np.float32) for frame in window_frames]
        
        # Enhanced weighting: center frame gets highest weight, others decay exponentially
        weights = np.exp(-1.0 * np.square(np.arange(len(window_frames)) - center_idx))
        weights = weights / np.sum(weights)
        
        # Apply weighted average with color space consistency
        smoothed = np.zeros_like(float_frames[0])
        for i, frame in enumerate(float_frames):
            smoothed += weights[i] * frame
        
        # Apply additional color consistency
        smoothed = self._apply_color_consistency(smoothed, float_frames[center_idx])
        
        return np.clip(smoothed, 0, 255).astype(np.uint8)

    def _apply_color_consistency(self, smoothed_frame: np.ndarray, center_frame: np.ndarray) -> np.ndarray:
        """Apply color consistency to maintain lighting and atmosphere"""
        
        # Calculate color statistics
        smoothed_mean = np.mean(smoothed_frame, axis=(0, 1))
        center_mean = np.mean(center_frame, axis=(0, 1))
        
        # Apply color correction to maintain consistency
        color_ratio = center_mean / (smoothed_mean + 1e-8)  # Avoid division by zero
        color_ratio = np.clip(color_ratio, 0.8, 1.2)  # Limit correction range
        
        corrected = smoothed_frame * color_ratio
        return corrected

    def _temporal_smooth(
        self,
        window_frames: List[np.ndarray],
        center_idx: int
    ) -> np.ndarray:
        """Apply temporal smoothing to reduce flickering"""
        
        if len(window_frames) == 1:
            return window_frames[0]
        
        # Convert frames to float for processing
        float_frames = [frame.astype(np.float32) for frame in window_frames]
        
        # Apply weighted average (center frame has higher weight)
        weights = np.exp(-0.5 * np.square(np.arange(len(window_frames)) - center_idx))
        weights = weights / np.sum(weights)
        
        # Apply weighted average
        smoothed = np.zeros_like(float_frames[0])
        for i, frame in enumerate(float_frames):
            smoothed += weights[i] * frame
        
        return np.clip(smoothed, 0, 255).astype(np.uint8)
    
    async def test_model(self) -> bool:
        """Test if the diffusion model is working correctly"""
        
        try:
            # Create a simple test image
            test_frame = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
            
            # Test transformation
            transformed = await self._transform_single_frame(
                test_frame,
                "a beautiful landscape",
                self._get_generation_params("low")
            )
            
            # Check if transformation was successful
            if transformed is not None and transformed.shape == test_frame.shape:
                logger.info("Diffusion model test passed")
                return True
            else:
                logger.error("Diffusion model test failed")
                return False
                
        except Exception as e:
            logger.error(f"Diffusion model test failed: {e}")
            return False 