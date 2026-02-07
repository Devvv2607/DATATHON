"""GROQ API integration service"""
import os
import time
from groq import Groq
from models import ErrorResponse


class GroqService:
    """Manages interactions with GROQ API"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize GROQ service.
        
        Args:
            api_key: GROQ API key (defaults to environment variable)
        """
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        try:
            self.client = Groq(api_key=self.api_key)
        except Exception as e:
            raise ValueError(f"Failed to initialize GROQ client: {str(e)}")
        
        self.max_retries = 2
        self.retry_delays = [1, 2, 4]
    
    def generate_analysis(
        self,
        prompt: str,
        system_context: str,
        temperature: float = 0.7
    ) -> str:
        """
        Generate analysis using GROQ API.
        
        Args:
            prompt: User prompt for analysis
            system_context: System context/instructions
            temperature: Sampling temperature (0-2)
            
        Returns:
            Generated text response
            
        Raises:
            Exception: If API call fails after retries
        """
        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[
                        {"role": "system", "content": system_context},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                    max_tokens=2000
                )
                
                # Extract the response content
                if response.choices and len(response.choices) > 0:
                    return response.choices[0].message.content
                else:
                    raise Exception("Empty response from GROQ API")
                
            except Exception as e:
                error_msg = str(e).lower()
                
                # Check for rate limiting
                if "rate" in error_msg or "429" in error_msg:
                    if attempt < self.max_retries:
                        wait_time = self.retry_delays[attempt]
                        print(f"Rate limited. Waiting {wait_time}s before retry...")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise Exception("GROQ API rate limit exceeded. Please try again later.")
                
                # Check for authentication errors
                if "auth" in error_msg or "401" in error_msg or "403" in error_msg:
                    raise Exception("Invalid GROQ API key")
                
                # Check for service unavailability
                if "503" in error_msg or "502" in error_msg or "unavailable" in error_msg:
                    if attempt < self.max_retries:
                        wait_time = self.retry_delays[attempt]
                        print(f"Service unavailable. Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise Exception("GROQ service temporarily unavailable")
                
                # For other errors, retry once then fail
                if attempt < self.max_retries:
                    time.sleep(self.retry_delays[attempt])
                    continue
                else:
                    raise Exception(f"GROQ API error: {str(e)}")
        
        raise Exception("Failed to get response from GROQ API")
