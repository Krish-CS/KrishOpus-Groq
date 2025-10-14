"""
Groq Client - Wrapper for Groq API
Supports both environment variable and .env file
"""

import os
from groq import Groq
from dotenv import load_dotenv


class GroqClient:
    """
    Wrapper for Groq AI API
    Loads API key from .env file OR environment variable
    """
    
    def __init__(self):
        """Initialize Groq client"""
        # Load .env file (if exists)
        load_dotenv()
        
        # Get API key
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            raise ValueError(
                "❌ GROQ_API_KEY not found!\n\n"
                "OPTION 1 - Create .env file in backend/ folder:\n"
                "   GROQ_API_KEY=gsk_your_key_here\n\n"
                "OPTION 2 - Set environment variable (PowerShell):\n"
                "   $env:GROQ_API_KEY = 'gsk_your_key_here'\n\n"
                "Get your key from: https://console.groq.com/keys"
            )
        
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"  # Default model
        
        print(f"✅ GroqClient initialized")
        print(f"   Model: {self.model}")
        print(f"   API Key: {api_key[:20]}...{api_key[-4:]}")
    
    def generate_text(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        model: str = None
    ) -> str:
        """
        Generate text using Groq API
        
        Args:
            prompt: Input prompt
            temperature: Creativity (0.0-1.0)
            max_tokens: Maximum response length
            model: Model name (defaults to llama-3.3-70b-versatile)
        
        Returns:
            Generated text
        """
        try:
            response = self.client.chat.completions.create(
                model=model or self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"❌ Groq API error: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Test if Groq API is working"""
        try:
            response = self.generate_text(
                prompt="Say 'Hello' in one word.",
                max_tokens=10
            )
            print(f"✅ Groq API test successful: {response}")
            return True
        except Exception as e:
            print(f"❌ Groq API test failed: {e}")
            return False
