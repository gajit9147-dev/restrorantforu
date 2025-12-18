import os
from typing import List, Dict, Any
import openai  # or anthropic, cohere, etc.
from agent import RestaurantAssistantAgent

class LLMEnhancedAgent(RestaurantAssistantAgent):
    """Enhanced agent with actual LLM integration"""
    
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        super().__init__(llm_provider="openai", model=model)
        
        # Configure LLM
        if api_key:
            openai.api_key = api_key
        else:
            openai.api_key = os.getenv("OPENAI_API_KEY")
        
        self.model = model
    
    def generate_llm_response(self, messages: List[Dict[str, str]]) -> str:
        """Generate response using actual LLM"""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
                functions=self._get_tools_schema(),
                function_call="auto"
            )
            
            return response.choices[0].message
            
        except Exception as e:
            return f"Error calling LLM: {str(e)}"
    
    def _get_tools_schema(self) -> List[Dict[str, Any]]:
        """Define tools for function calling"""
        return [
            {
                "name": "get_booking_details",
                "description": "Retrieve booking details by ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "booking_id": {
                            "type": "string",
                            "description": "Booking reference number"
                        }
                    },
                    "required": ["booking_id"]
                }
            },
            {
                "name": "delete_booking",
                "description": "Cancel/delete a booking",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "booking_id": {
                            "type": "string",
                            "description": "Booking reference number"
                        }
                    },
                    "required": ["booking_id"]
                }
            },
            {
                "name": "search_knowledge_base",
                "description": "Search restaurant information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query"
                        }
                    },
                    "required": ["query"]
                }
            }
        ]