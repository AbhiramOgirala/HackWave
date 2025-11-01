import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class GeminiService:
    """Service for interacting with Google Gemini API"""
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.vision_model = genai.GenerativeModel('gemini-2.5-flash')
    
    async def analyze_cultural_context(self, text: str, language: str = "en") -> dict:
        """
        Analyze text for cultural context using Gemini API
        
        Args:
            text: The input text to analyze
            language: Language code (default: en)
        
        Returns:
            Dictionary with cultural analysis results
        """
        
        prompt = f"""
You are a cultural and historical expert. Analyze the following text and provide detailed insights in exactly 4 sections.

Text to analyze: "{text}"
Language: {language}

Please provide your analysis in the following JSON format:

{{
    "cultural_origin": "Detailed explanation of which culture this text is primarily related to, including time period, geographical region, and cultural significance. Be specific and comprehensive.",
    "cross_cultural_connections": "Detailed explanation of how this text, concept, or cultural element relates to or influenced other cultures. Include specific examples of cultural exchange, similarities, or adaptations in different cultures.",
    "modern_analogy": "Provide a clear and relatable modern-day analogy or parallel that helps contemporary readers understand this cultural concept. Explain how the historical/cultural element compares to something familiar in today's world.",
    "visualization_description": "Describe in detail what kind of image or visual representation would best illustrate this cultural context. Be specific about elements, colors, symbols, setting, and mood that should be included in a visualization."
}}

Important: 
- Provide substantial, educational content in each section (at least 3-4 sentences each)
- Be accurate and factual
- Make connections clear and meaningful
- Ensure the modern analogy is truly relatable
- Return ONLY valid JSON, no additional text
"""
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Clean up the response to extract JSON
            # Remove markdown code blocks if present
            result_text = re.sub(r'^```json\s*', '', result_text)
            result_text = re.sub(r'^```\s*', '', result_text)
            result_text = re.sub(r'\s*```$', '', result_text)
            result_text = result_text.strip()
            
            # Parse JSON response
            analysis = json.loads(result_text)
            
            # Validate required fields
            required_fields = [
                "cultural_origin",
                "cross_cultural_connections", 
                "modern_analogy",
                "visualization_description"
            ]
            
            for field in required_fields:
                if field not in analysis:
                    raise ValueError(f"Missing required field: {field}")
            
            return analysis
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response text: {result_text}")
            # Return a structured error response
            return {
                "cultural_origin": "Error parsing response from AI model.",
                "cross_cultural_connections": "Please try again with different text.",
                "modern_analogy": "The analysis could not be completed.",
                "visualization_description": "No visualization available."
            }
        except Exception as e:
            print(f"Error in cultural analysis: {e}")
            return {
                "cultural_origin": f"Error: {str(e)}",
                "cross_cultural_connections": "Analysis failed.",
                "modern_analogy": "Please check your API key and try again.",
                "visualization_description": "No visualization available."
            }
    
    async def generate_image_description(self, visualization_desc: str) -> str:
        """
        Generate a detailed prompt for image generation based on visualization description
        
        Args:
            visualization_desc: Description of what to visualize
        
        Returns:
            Enhanced prompt for image generation
        """
        
        prompt = f"""
Based on this cultural visualization description, create a detailed, specific prompt for generating an educational illustration:

Description: {visualization_desc}

Create a prompt that:
- Specifies artistic style (e.g., historical illustration, modern infographic, traditional art style)
- Includes specific visual elements, colors, and composition
- Mentions cultural accuracy and educational value
- Is suitable for an AI image generator

Return only the image generation prompt, nothing else.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating image description: {e}")
            return visualization_desc


# Create singleton instance
gemini_service = GeminiService()
