"""
AI Creative Director endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from loguru import logger

from app.services.llm.creative_director import CreativeDirector

router = APIRouter()


class ChatMessage(BaseModel):
    """Chat message model"""
    role: str  # user, assistant
    content: str
    timestamp: Optional[str] = None


class ChatRequest(BaseModel):
    """Chat request model"""
    message: str
    conversation_history: List[ChatMessage] = []
    video_context: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response model"""
    message: str
    suggestions: List[str] = []
    prompt_refinements: List[str] = []
    confidence: float


class PromptSuggestion(BaseModel):
    """Prompt suggestion model"""
    prompt: str
    description: str
    category: str  # atmosphere, weather, time_of_day, style


@router.post("/chat", response_model=ChatResponse)
async def chat_with_director(request: ChatRequest):
    """Chat with the AI Creative Director for prompt assistance"""
    
    try:
        director = CreativeDirector()
        
        # Process the chat request
        response = await director.process_message(
            request.message,
            request.conversation_history,
            request.video_context
        )
        
        return ChatResponse(
            message=response["message"],
            suggestions=response.get("suggestions", []),
            prompt_refinements=response.get("prompt_refinements", []),
            confidence=response.get("confidence", 0.8)
        )
        
    except Exception as e:
        logger.error(f"Error in AI director chat: {e}")
        raise HTTPException(status_code=500, detail="Failed to process chat request")


@router.get("/suggestions", response_model=List[PromptSuggestion])
async def get_prompt_suggestions(category: Optional[str] = None):
    """Get prompt suggestions from the AI Creative Director"""
    
    try:
        director = CreativeDirector()
        suggestions = await director.get_suggestions(category)
        
        return [
            PromptSuggestion(
                prompt=suggestion["prompt"],
                description=suggestion["description"],
                category=suggestion["category"]
            )
            for suggestion in suggestions
        ]
        
    except Exception as e:
        logger.error(f"Error getting prompt suggestions: {e}")
        raise HTTPException(status_code=500, detail="Failed to get suggestions")


@router.post("/analyze-video")
async def analyze_video_context(video_description: str):
    """Analyze video context and provide transformation suggestions"""
    
    try:
        director = CreativeDirector()
        analysis = await director.analyze_video(video_description)
        
        return {
            "analysis": analysis["analysis"],
            "suggestions": analysis["suggestions"],
            "mood": analysis["mood"],
            "potential_transformations": analysis["potential_transformations"]
        }
        
    except Exception as e:
        logger.error(f"Error analyzing video context: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze video context")


@router.post("/refine-prompt")
async def refine_prompt(
    original_prompt: str,
    feedback: str,
    desired_outcome: Optional[str] = None
):
    """Refine a prompt based on user feedback"""
    
    try:
        director = CreativeDirector()
        refined_prompt = await director.refine_prompt(
            original_prompt,
            feedback,
            desired_outcome
        )
        
        return {
            "original_prompt": original_prompt,
            "refined_prompt": refined_prompt["prompt"],
            "improvements": refined_prompt["improvements"],
            "confidence": refined_prompt["confidence"]
        }
        
    except Exception as e:
        logger.error(f"Error refining prompt: {e}")
        raise HTTPException(status_code=500, detail="Failed to refine prompt")


@router.get("/style-presets", response_model=List[dict])
async def get_style_presets():
    """Get available style presets for video transformation"""
    
    presets = [
        {
            "id": "cinematic",
            "name": "Cinematic",
            "description": "Hollywood-style cinematic look with dramatic lighting",
            "prompt_modifier": "cinematic lighting, professional film look, dramatic atmosphere"
        },
        {
            "id": "vintage",
            "name": "Vintage",
            "description": "Retro film look with warm tones and grain",
            "prompt_modifier": "vintage film look, warm tones, film grain, retro aesthetic"
        },
        {
            "id": "futuristic",
            "name": "Futuristic",
            "description": "Sci-fi aesthetic with neon lights and cyberpunk elements",
            "prompt_modifier": "futuristic, neon lights, cyberpunk, sci-fi aesthetic"
        },
        {
            "id": "natural",
            "name": "Natural",
            "description": "Clean, natural look with balanced colors",
            "prompt_modifier": "natural lighting, clean colors, balanced exposure"
        },
        {
            "id": "artistic",
            "name": "Artistic",
            "description": "Creative, artistic interpretation with unique styling",
            "prompt_modifier": "artistic interpretation, creative styling, unique visual approach"
        }
    ]
    
    return presets


@router.get("/atmosphere-options", response_model=List[dict])
async def get_atmosphere_options():
    """Get available atmosphere options for video transformation"""
    
    atmospheres = [
        {
            "category": "time_of_day",
            "options": [
                "sunrise", "morning", "noon", "afternoon", "sunset", "twilight", "night", "midnight"
            ]
        },
        {
            "category": "weather",
            "options": [
                "clear", "cloudy", "rainy", "stormy", "foggy", "misty", "snowy", "windy"
            ]
        },
        {
            "category": "season",
            "options": [
                "spring", "summer", "autumn", "winter"
            ]
        },
        {
            "category": "mood",
            "options": [
                "peaceful", "dramatic", "mysterious", "energetic", "melancholic", "romantic", "tense"
            ]
        }
    ]
    
    return atmospheres


@router.post("/generate-prompt")
async def generate_prompt_from_conditions(
    conditions: List[str],
    style_preset: Optional[str] = None,
    video_context: Optional[str] = None
):
    """Generate a comprehensive prompt from selected conditions"""
    
    try:
        director = CreativeDirector()
        prompt = await director.generate_prompt_from_conditions(
            conditions,
            style_preset,
            video_context
        )
        
        return {
            "prompt": prompt["prompt"],
            "breakdown": prompt["breakdown"],
            "confidence": prompt["confidence"],
            "suggestions": prompt["suggestions"]
        }
        
    except Exception as e:
        logger.error(f"Error generating prompt: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate prompt") 