"""
Video processing service for Project Aura
"""

import cv2
import numpy as np
from typing import List, Tuple
import os
from loguru import logger
from app.core.config import settings


class VideoProcessor:
    """Handles video processing operations"""
    
    def __init__(self):
        self.target_fps = settings.TARGET_FPS
        self.max_resolution = settings.MAX_RESOLUTION
    
    async def extract_frames(self, video_path: str) -> List[np.ndarray]:
        """Extract frames from video file"""
        
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise ValueError(f"Could not open video file: {video_path}")
            
            frames = []
            frame_count = 0
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            logger.info(f"Processing video: {total_frames} frames at {fps} FPS")
            
            # Calculate frame sampling rate to achieve target FPS
            if fps > self.target_fps:
                sample_rate = int(fps / self.target_fps)
            else:
                sample_rate = 1
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Sample frames based on target FPS
                if frame_count % sample_rate == 0:
                    # Resize frame if necessary
                    frame = self._resize_frame(frame)
                    frames.append(frame)
                
                frame_count += 1
                
                # Progress logging
                if frame_count % 100 == 0:
                    logger.info(f"Processed {frame_count}/{total_frames} frames")
            
            cap.release()
            
            logger.info(f"Extracted {len(frames)} frames from video")
            return frames
            
        except Exception as e:
            logger.error(f"Error extracting frames: {e}")
            raise
    
    async def create_video(
        self, 
        frames: List[np.ndarray], 
        output_path: str,
        fps: int = None
    ) -> str:
        """Create video from frames"""
        
        if not frames:
            raise ValueError("No frames provided")
        
        try:
            fps = fps or self.target_fps
            height, width = frames[0].shape[:2]
            
            # Define video codec
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            
            # Create video writer
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            logger.info(f"Creating video: {len(frames)} frames at {fps} FPS")
            
            for i, frame in enumerate(frames):
                # Ensure frame is in BGR format for OpenCV
                if len(frame.shape) == 3 and frame.shape[2] == 3:
                    # Convert RGB to BGR if necessary
                    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                else:
                    frame_bgr = frame
                
                out.write(frame_bgr)
                
                # Progress logging
                if i % 100 == 0:
                    logger.info(f"Written {i}/{len(frames)} frames")
            
            out.release()
            
            logger.info(f"Video created successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating video: {e}")
            raise
    
    def _resize_frame(self, frame: np.ndarray) -> np.ndarray:
        """Resize frame to target resolution while maintaining aspect ratio"""
        
        height, width = frame.shape[:2]
        target_width, target_height = self.max_resolution
        
        # Calculate scaling factor
        scale = min(target_width / width, target_height / height)
        
        if scale < 1:
            new_width = int(width * scale)
            new_height = int(height * scale)
            frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        return frame
    
    async def get_video_info(self, video_path: str) -> dict:
        """Get video information"""
        
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise ValueError(f"Could not open video file: {video_path}")
            
            info = {
                "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                "fps": cap.get(cv2.CAP_PROP_FPS),
                "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                "duration": cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS),
                "file_size": os.path.getsize(video_path)
            }
            
            cap.release()
            return info
            
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            raise
    
    async def validate_video(self, video_path: str) -> bool:
        """Validate video file"""
        
        try:
            # Check if file exists
            if not os.path.exists(video_path):
                return False
            
            # Check file size
            file_size = os.path.getsize(video_path)
            if file_size > settings.MAX_FILE_SIZE:
                return False
            
            # Check if it's a valid video file
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return False
            
            # Check duration
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            duration = frame_count / fps if fps > 0 else 0
            
            cap.release()
            
            if duration > settings.MAX_VIDEO_DURATION:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating video: {e}")
            return False
    
    async def create_thumbnail(self, video_path: str, output_path: str) -> str:
        """Create thumbnail from video"""
        
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise ValueError(f"Could not open video file: {video_path}")
            
            # Get middle frame
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            middle_frame = total_frames // 2
            
            cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame)
            ret, frame = cap.read()
            
            if not ret:
                raise ValueError("Could not read frame for thumbnail")
            
            cap.release()
            
            # Resize thumbnail
            frame = self._resize_frame(frame)
            
            # Save thumbnail
            cv2.imwrite(output_path, frame)
            
            logger.info(f"Thumbnail created: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating thumbnail: {e}")
            raise
    
    async def apply_temporal_consistency(
        self, 
        frames: List[np.ndarray], 
        window_size: int = 5
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
            
            logger.info(f"Applied temporal consistency to {len(frames)} frames")
            return consistent_frames
            
        except Exception as e:
            logger.error(f"Error applying temporal consistency: {e}")
            return frames
    
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