"""
AI Creative Director service for Project Aura
"""

from typing import List, Dict, Optional
from loguru import logger
import json
import random


class CreativeDirector:
    """AI Creative Director for video transformation assistance"""
    
    def __init__(self):
        self.conversation_context = {}
        self.prompt_templates = self._load_prompt_templates()
        self.suggestions_database = self._load_suggestions_database()
    
    async def process_message(
        self,
        message: str,
        conversation_history: List[Dict] = None,
        video_context: Optional[str] = None
    ) -> Dict:
        """Process user message and provide creative assistance"""
        
        try:
            # Analyze user intent
            intent = self._analyze_intent(message)
            
            # Generate response based on intent
            if intent == "prompt_help":
                response = await self._provide_prompt_help(message, video_context)
            elif intent == "style_advice":
                response = await self._provide_style_advice(message, video_context)
            elif intent == "technical_help":
                response = await self._provide_technical_help(message)
            elif intent == "general_question":
                response = await self._provide_general_response(message)
            else:
                response = await self._provide_general_response(message)
            
            # Add suggestions and refinements
            response["suggestions"] = self._generate_suggestions(message, video_context)
            response["prompt_refinements"] = self._generate_prompt_refinements(message)
            response["confidence"] = 0.85
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return {
                "message": "I apologize, but I'm having trouble processing your request. Could you please rephrase it?",
                "suggestions": [],
                "prompt_refinements": [],
                "confidence": 0.5
            }
    
    async def get_suggestions(self, category: Optional[str] = None) -> List[Dict]:
        """Get prompt suggestions based on category"""
        
        try:
            if category and category in self.suggestions_database:
                return self.suggestions_database[category]
            elif category:
                return []
            else:
                # Return suggestions from all categories
                all_suggestions = []
                for cat_suggestions in self.suggestions_database.values():
                    all_suggestions.extend(cat_suggestions)
                return random.sample(all_suggestions, min(10, len(all_suggestions)))
                
        except Exception as e:
            logger.error(f"Error getting suggestions: {e}")
            return []
    
    async def analyze_video(self, video_description: str) -> Dict:
        """Analyze video context and provide transformation suggestions"""
        
        try:
            # Extract key elements from video description
            elements = self._extract_video_elements(video_description)
            
            # Generate analysis
            analysis = {
                "analysis": f"Based on your video description, I can see {elements['primary_elements']}. "
                           f"The overall mood appears to be {elements['mood']}, "
                           f"and the lighting conditions are {elements['lighting']}.",
                "suggestions": self._generate_video_suggestions(elements),
                "mood": elements["mood"],
                "potential_transformations": self._get_potential_transformations(elements)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing video: {e}")
            return {
                "analysis": "I'm having trouble analyzing your video description. Could you provide more details?",
                "suggestions": [],
                "mood": "unknown",
                "potential_transformations": []
            }
    
    async def refine_prompt(
        self,
        original_prompt: str,
        feedback: str,
        desired_outcome: Optional[str] = None
    ) -> Dict:
        """Refine a prompt based on user feedback"""
        
        try:
            # Analyze feedback
            feedback_analysis = self._analyze_feedback(feedback)
            
            # Generate refined prompt
            refined_prompt = self._apply_feedback_to_prompt(
                original_prompt, feedback_analysis, desired_outcome
            )
            
            return {
                "prompt": refined_prompt,
                "improvements": feedback_analysis["improvements"],
                "confidence": 0.9
            }
            
        except Exception as e:
            logger.error(f"Error refining prompt: {e}")
            return {
                "prompt": original_prompt,
                "improvements": ["Unable to process feedback"],
                "confidence": 0.5
            }
    
    async def generate_prompt_from_conditions(
        self,
        conditions: List[str],
        style_preset: Optional[str] = None,
        video_context: Optional[str] = None
    ) -> Dict:
        """Generate a comprehensive prompt from selected conditions"""
        
        try:
            # Build prompt from conditions
            base_prompt = self._build_prompt_from_conditions(conditions)
            
            # Add style preset if provided
            if style_preset:
                base_prompt = self._add_style_preset(base_prompt, style_preset)
            
            # Enhance with video context if provided
            if video_context:
                base_prompt = self._enhance_with_context(base_prompt, video_context)
            
            return {
                "prompt": base_prompt,
                "breakdown": self._explain_prompt_breakdown(conditions, style_preset),
                "confidence": 0.95,
                "suggestions": self._generate_additional_suggestions(conditions)
            }
            
        except Exception as e:
            logger.error(f"Error generating prompt from conditions: {e}")
            return {
                "prompt": "a beautiful scene",
                "breakdown": "Basic prompt due to error",
                "confidence": 0.5,
                "suggestions": []
            }
    
    def _analyze_intent(self, message: str) -> str:
        """Analyze user intent from message"""
        
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["prompt", "describe", "what should i say"]):
            return "prompt_help"
        elif any(word in message_lower for word in ["style", "look", "aesthetic", "mood"]):
            return "style_advice"
        elif any(word in message_lower for word in ["how", "technical", "settings", "quality"]):
            return "technical_help"
        else:
            return "general_question"
    
    async def _provide_prompt_help(self, message: str, video_context: Optional[str]) -> Dict:
        """Provide help with prompt creation"""
        
        suggestions = [
            "Try describing the atmosphere you want: 'a foggy autumn morning'",
            "Include lighting details: 'golden hour lighting with warm tones'",
            "Mention weather conditions: 'stormy night with rain'",
            "Specify time of day: 'sunset with dramatic clouds'",
            "Add mood elements: 'peaceful and serene atmosphere'"
        ]
        
        return {
            "message": "I'd be happy to help you create the perfect prompt! "
                      "Think about the atmosphere, lighting, weather, and mood you want to achieve. "
                      "Be specific but concise. What kind of transformation are you looking for?"
        }
    
    async def _provide_style_advice(self, message: str, video_context: Optional[str]) -> Dict:
        """Provide style and aesthetic advice"""
        
        return {
            "message": "For style guidance, consider these approaches:\n"
                      "• Cinematic: Dramatic lighting, professional film look\n"
                      "• Vintage: Warm tones, film grain, retro aesthetic\n"
                      "• Futuristic: Neon lights, cyberpunk elements\n"
                      "• Natural: Clean, balanced colors and lighting\n"
                      "• Artistic: Creative interpretation with unique styling"
        }
    
    async def _provide_technical_help(self, message: str) -> Dict:
        """Provide technical assistance"""
        
        return {
            "message": "For technical questions:\n"
                      "• Quality settings affect processing time and output quality\n"
                      "• Longer videos may take more time to process\n"
                      "• Higher quality settings produce better results but take longer\n"
                      "• The system preserves motion and structure from your original video"
        }
    
    async def _provide_general_response(self, message: str) -> Dict:
        """Provide general response"""
        
        return {
            "message": "I'm here to help you create amazing video transformations! "
                      "I can assist with prompt creation, style advice, and technical questions. "
                      "What would you like to know about?"
        }
    
    def _generate_suggestions(self, message: str, video_context: Optional[str]) -> List[str]:
        """Generate contextual suggestions"""
        
        suggestions = [
            "Try 'a misty forest at dawn' for a mysterious atmosphere",
            "Consider 'urban night scene with neon reflections' for city vibes",
            "Experiment with 'stormy ocean waves at sunset' for dramatic effect",
            "Test 'peaceful garden in spring morning' for tranquility"
        ]
        
        return random.sample(suggestions, 2)
    
    def _generate_prompt_refinements(self, message: str) -> List[str]:
        """Generate prompt refinements"""
        
        refinements = [
            "Add more specific lighting details",
            "Include weather conditions for atmosphere",
            "Specify time of day for mood",
            "Mention color palette preferences"
        ]
        
        return random.sample(refinements, 2)
    
    def _load_prompt_templates(self) -> Dict:
        """Load prompt templates"""
        
        return {
            "atmosphere": [
                "a {weather} {time_of_day} scene",
                "a {mood} atmosphere with {lighting}",
                "a {season} {weather} day"
            ],
            "style": [
                "{style} aesthetic with {mood} mood",
                "{style} lighting and {atmosphere} atmosphere"
            ]
        }
    
    def _load_suggestions_database(self) -> Dict:
        """Load suggestions database"""
        
        return {
            "atmosphere": [
                {"prompt": "a foggy autumn morning", "description": "Mysterious and peaceful", "category": "atmosphere"},
                {"prompt": "stormy night with lightning", "description": "Dramatic and intense", "category": "atmosphere"},
                {"prompt": "golden hour sunset", "description": "Warm and romantic", "category": "atmosphere"}
            ],
            "weather": [
                {"prompt": "rainy city streets", "description": "Urban melancholy", "category": "weather"},
                {"prompt": "snowy mountain landscape", "description": "Pure and serene", "category": "weather"},
                {"prompt": "misty forest path", "description": "Mysterious and enchanting", "category": "weather"}
            ],
            "time_of_day": [
                {"prompt": "dawn breaking over horizon", "description": "New beginnings", "category": "time_of_day"},
                {"prompt": "midnight city lights", "description": "Urban nightlife", "category": "time_of_day"},
                {"prompt": "afternoon sunlight through trees", "description": "Natural warmth", "category": "time_of_day"}
            ],
            "style": [
                {"prompt": "cinematic noir lighting", "description": "Film noir aesthetic", "category": "style"},
                {"prompt": "vintage sepia tones", "description": "Retro film look", "category": "style"},
                {"prompt": "futuristic neon glow", "description": "Cyberpunk aesthetic", "category": "style"}
            ]
        }
    
    def _extract_video_elements(self, description: str) -> Dict:
        """Extract key elements from video description"""
        
        # Simple keyword extraction (in production, use NLP)
        description_lower = description.lower()
        
        elements = {
            "primary_elements": "various elements",
            "mood": "neutral",
            "lighting": "natural",
            "setting": "general"
        }
        
        # Extract mood
        if any(word in description_lower for word in ["dark", "moody", "dramatic"]):
            elements["mood"] = "dramatic"
        elif any(word in description_lower for word in ["bright", "cheerful", "happy"]):
            elements["mood"] = "cheerful"
        elif any(word in description_lower for word in ["peaceful", "calm", "serene"]):
            elements["mood"] = "peaceful"
        
        # Extract lighting
        if any(word in description_lower for word in ["dark", "night", "low light"]):
            elements["lighting"] = "low"
        elif any(word in description_lower for word in ["bright", "sunny", "daylight"]):
            elements["lighting"] = "bright"
        
        return elements
    
    def _generate_video_suggestions(self, elements: Dict) -> List[str]:
        """Generate video-specific suggestions"""
        
        suggestions = []
        
        if elements["mood"] == "dramatic":
            suggestions.extend([
                "Try adding stormy weather for intensity",
                "Consider low-key lighting for drama",
                "Experiment with high contrast settings"
            ])
        elif elements["mood"] == "peaceful":
            suggestions.extend([
                "Add soft, diffused lighting",
                "Consider natural elements like trees or water",
                "Use warm, golden tones"
            ])
        
        return suggestions[:3]
    
    def _get_potential_transformations(self, elements: Dict) -> List[str]:
        """Get potential transformation suggestions"""
        
        transformations = [
            "Convert to different time of day",
            "Change weather conditions",
            "Apply cinematic lighting",
            "Add atmospheric effects"
        ]
        
        return transformations
    
    def _analyze_feedback(self, feedback: str) -> Dict:
        """Analyze user feedback"""
        
        feedback_lower = feedback.lower()
        
        improvements = []
        
        if any(word in feedback_lower for word in ["too dark", "brighten", "lighter"]):
            improvements.append("Increase brightness and exposure")
        
        if any(word in feedback_lower for word in ["too bright", "darker", "dim"]):
            improvements.append("Reduce brightness and add shadows")
        
        if any(word in feedback_lower for word in ["blurry", "sharp", "clear"]):
            improvements.append("Enhance sharpness and detail")
        
        if any(word in feedback_lower for word in ["color", "tone", "hue"]):
            improvements.append("Adjust color balance and saturation")
        
        return {"improvements": improvements}
    
    def _apply_feedback_to_prompt(self, original_prompt: str, feedback_analysis: Dict, desired_outcome: Optional[str]) -> str:
        """Apply feedback to improve prompt"""
        
        improved_prompt = original_prompt
        
        for improvement in feedback_analysis["improvements"]:
            if "brightness" in improvement.lower():
                improved_prompt += ", bright lighting, high exposure"
            elif "shadows" in improvement.lower():
                improved_prompt += ", dramatic shadows, low key lighting"
            elif "sharpness" in improvement.lower():
                improved_prompt += ", sharp details, crisp focus"
            elif "color" in improvement.lower():
                improved_prompt += ", vibrant colors, rich saturation"
        
        if desired_outcome:
            improved_prompt += f", {desired_outcome}"
        
        return improved_prompt
    
    def _build_prompt_from_conditions(self, conditions: List[str]) -> str:
        """Build prompt from conditions"""
        
        if not conditions:
            return "a beautiful scene"
        
        # Combine conditions intelligently
        prompt_parts = []
        
        for condition in conditions:
            if "time" in condition.lower():
                prompt_parts.insert(0, condition)  # Time usually goes first
            elif "weather" in condition.lower():
                prompt_parts.append(condition)
            elif "mood" in condition.lower():
                prompt_parts.append(condition)
            else:
                prompt_parts.append(condition)
        
        return ", ".join(prompt_parts)
    
    def _add_style_preset(self, prompt: str, style_preset: str) -> str:
        """Add style preset to prompt"""
        
        style_modifiers = {
            "cinematic": "cinematic lighting, professional film look",
            "vintage": "vintage film look, warm tones, film grain",
            "futuristic": "futuristic, neon lights, cyberpunk aesthetic",
            "natural": "natural lighting, clean colors",
            "artistic": "artistic interpretation, creative styling"
        }
        
        if style_preset in style_modifiers:
            prompt += f", {style_modifiers[style_preset]}"
        
        return prompt
    
    def _enhance_with_context(self, prompt: str, video_context: str) -> str:
        """Enhance prompt with video context"""
        
        # Simple context enhancement (in production, use more sophisticated NLP)
        context_lower = video_context.lower()
        
        if "city" in context_lower or "urban" in context_lower:
            prompt += ", urban environment"
        elif "nature" in context_lower or "outdoor" in context_lower:
            prompt += ", natural environment"
        elif "indoor" in context_lower:
            prompt += ", indoor setting"
        
        return prompt
    
    def _explain_prompt_breakdown(self, conditions: List[str], style_preset: Optional[str]) -> str:
        """Explain the prompt breakdown"""
        
        explanation = f"Your prompt combines {len(conditions)} conditions"
        
        if conditions:
            explanation += f": {', '.join(conditions)}"
        
        if style_preset:
            explanation += f" with a {style_preset} style preset"
        
        return explanation
    
    def _generate_additional_suggestions(self, conditions: List[str]) -> List[str]:
        """Generate additional suggestions based on conditions"""
        
        suggestions = []
        
        if "night" in str(conditions).lower():
            suggestions.append("Consider adding 'moonlight' or 'street lights' for night scenes")
        
        if "rain" in str(conditions).lower():
            suggestions.append("Try adding 'wet surfaces' or 'reflections' for rain effects")
        
        if "fog" in str(conditions).lower():
            suggestions.append("Consider 'misty atmosphere' or 'soft focus' for fog effects")
        
        return suggestions[:2] 