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
You are a cultural and historical expert. Analyze the following text and provide detailed insights.

Text to analyze: "{text}"
Language: {language}

Please provide your analysis in the following JSON format:

{{
    "cultural_origin": "Detailed explanation of which culture this text is primarily related to, including time period, geographical region, and cultural significance. Be specific and comprehensive.",
    "cross_cultural_connections": "Detailed explanation of how this text, concept, or cultural element relates to or influenced other cultures. Include specific examples of cultural exchange, similarities, or adaptations in different cultures.",
    "modern_analogy": "Provide a SOPHISTICATED and TAILORED modern-day analogy that goes beyond surface-level comparisons. Connect to contemporary student experiences like social media, technology, pop culture, current events, or everyday life. Make it relatable to Gen Z/Millennial perspectives while maintaining educational depth. Avoid generic comparisons.",
    "visualization_description": "Describe in detail what kind of image or visual representation would best illustrate this cultural context. Be specific about elements, colors, symbols, setting, and mood that should be included in a visualization.",
    "timeline_events": [
        {{
            "year": "YYYY or BCE/CE format",
            "title": "Brief event title",
            "description": "What happened and why it matters",
            "significance": "Impact on culture/history"
        }}
    ],
    "geographic_locations": [
        {{
            "name": "Location name",
            "coordinates": {{"lat": 0.0, "lng": 0.0}},
            "significance": "Why this location matters to the cultural context",
            "modern_name": "Current name if different"
        }}
    ],
    "key_concepts": [
        {{
            "term": "Important term or concept",
            "definition": "Clear, student-friendly explanation",
            "context": "How it relates to the main topic",
            "modern_parallel": "Contemporary equivalent or example"
        }}
    ],
    "external_resources": {{
        "timeline_links": ["URL to interactive timeline resources if available"],
        "map_links": ["URL to interactive map resources if available"],
        "educational_videos": ["URL to educational video resources"],
        "further_reading": ["URL to articles or educational content"]
    }}
}}

CRITICAL INSTRUCTIONS - CONDITIONAL FIELDS:
1. **timeline_events**: ONLY include if the text has clear historical context with specific dates/periods. 
   - Include 3-5 events in chronological order if applicable
   - Return EMPTY ARRAY [] if text is modern, theoretical, or has no historical timeline
   
2. **geographic_locations**: ONLY include if specific places/locations are relevant to understanding the text.
   - Include 2-4 locations with ACCURATE coordinates (verify they're real places)
   - Return EMPTY ARRAY [] if the text is abstract, philosophical, or not location-specific
   
3. **key_concepts**: ONLY include if there are cultural/technical terms that need explanation.
   - Include 3-5 important concepts that students may not know
   - Return EMPTY ARRAY [] if text uses only common terminology
   
4. **external_resources**: ONLY include REAL, VERIFIED URLs from reputable sources.
   - Use actual URLs from: Khan Academy, National Geographic, BBC, Britannica, educational YouTube channels
   - Return EMPTY OBJECT {{}} if you cannot provide verified resources
   - DO NOT invent or guess URLs

5. **modern_analogy**: ALWAYS required - make it SPECIFIC and CREATIVE
   - Think: TikTok trends, streaming culture, app ecosystems, gaming, social media
   - Avoid generic comparisons like "like a library" or "like a book"

EXAMPLES OF WHEN TO INCLUDE/EXCLUDE:

✅ INCLUDE timeline_events:
- "The Ramayana is an ancient epic..." → Has clear historical periods
- "The Renaissance began in 14th century..." → Specific historical timeline

❌ EXCLUDE timeline_events:
- "Democracy is a form of government..." → Concept, not historical event
- "Mindfulness meditation involves..." → Practice, not tied to specific timeline

✅ INCLUDE geographic_locations:
- "The Silk Road connected China to Rome..." → Specific places matter
- "Shakespeare's Globe Theatre in London..." → Location is relevant

❌ EXCLUDE geographic_locations:
- "Poetry is a form of artistic expression..." → Abstract concept
- "The scientific method involves..." → No specific location needed

✅ INCLUDE key_concepts:
- "Buddhism emphasizes Nirvana and Karma..." → Specific terms need explanation
- "Renaissance Humanism focused on..." → Technical cultural term

❌ EXCLUDE key_concepts:
- "The cat sat on the mat..." → No complex concepts
- "Democracy means rule by the people..." → Already explained in text

Be accurate and factual. Return ONLY valid JSON, no additional text.
"""
        
        try:
            # Generate content with safety settings to avoid blocking
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 8192,
                }
            )
            
            # Check if response was blocked
            if not response or not response.text:
                print(f"⚠️ Response blocked or empty. Safety ratings: {response.prompt_feedback if response else 'No response'}")
                return {
                    "cultural_origin": "Unable to analyze this text. The content may have triggered safety filters or the AI couldn't process it.",
                    "cross_cultural_connections": "Please try rephrasing your text or use a different passage.",
                    "modern_analogy": "Analysis was blocked or failed.",
                    "visualization_description": "No visualization available.",
                    "timeline_events": [],
                    "geographic_locations": [],
                    "key_concepts": [],
                    "external_resources": {}
                }
            
            result_text = response.text.strip()
            print(f"🤖 AI Response length: {len(result_text)} characters")
            
            # Clean up the response to extract JSON
            # Remove markdown code blocks if present
            result_text = re.sub(r'^```json\s*', '', result_text, flags=re.IGNORECASE)
            result_text = re.sub(r'^```\s*', '', result_text)
            result_text = re.sub(r'\s*```$', '', result_text)
            result_text = result_text.strip()
            
            # Find the JSON object - extract from first { to last matching }
            # This handles cases where AI adds text before or after the JSON
            start_idx = result_text.find('{')
            if start_idx != -1:
                # Count braces to find the matching closing brace
                brace_count = 0
                end_idx = start_idx
                for i in range(start_idx, len(result_text)):
                    if result_text[i] == '{':
                        brace_count += 1
                    elif result_text[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end_idx = i + 1
                            break
                
                if end_idx > start_idx:
                    result_text = result_text[start_idx:end_idx]
            
            print(f"📝 Cleaned JSON length: {len(result_text)} characters")
            
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
            
            # Add default empty arrays if enhanced fields are missing
            if "timeline_events" not in analysis:
                analysis["timeline_events"] = []
            if "geographic_locations" not in analysis:
                analysis["geographic_locations"] = []
            if "key_concepts" not in analysis:
                analysis["key_concepts"] = []
            if "external_resources" not in analysis:
                analysis["external_resources"] = {}
            
            print(f"✅ Analysis completed successfully")
            print(f"   - Timeline events: {len(analysis.get('timeline_events', []))}")
            print(f"   - Geographic locations: {len(analysis.get('geographic_locations', []))}")
            print(f"   - Key concepts: {len(analysis.get('key_concepts', []))}")
            
            return analysis
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print(f"📄 Response text preview: {result_text[:500]}...")
            # Return a structured error response
            return {
                "cultural_origin": "Error: The AI returned invalid JSON format. This is usually temporary.",
                "cross_cultural_connections": "Please try again. If the issue persists, try simplifying your text.",
                "modern_analogy": "The analysis could not be completed due to formatting issues.",
                "visualization_description": "No visualization available.",
                "timeline_events": [],
                "geographic_locations": [],
                "key_concepts": [],
                "external_resources": {}
            }
        except Exception as e:
            print(f"❌ Error in cultural analysis: {e}")
            import traceback
            traceback.print_exc()
            return {
                "cultural_origin": f"Error: {str(e)}",
                "cross_cultural_connections": "Analysis failed. Please check your internet connection and API key.",
                "modern_analogy": "Please try again or contact support if the issue persists.",
                "visualization_description": "No visualization available.",
                "timeline_events": [],
                "geographic_locations": [],
                "key_concepts": [],
                "external_resources": {}
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
