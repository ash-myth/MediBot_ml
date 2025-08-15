"""
Configuration settings for the Symptom Checker
"""

import os
from typing import Optional

class Config:
    """Configuration management for the symptom checker"""
    
    # Gemini AI Configuration
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = "gemini-1.5-flash"  # Fast and accurate model
    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    
    # ML Model Configuration
    ML_CONFIDENCE_THRESHOLD = 0.15  # Minimum confidence for ML predictions
    ML_HIGH_CONFIDENCE = 0.7
    ML_MEDIUM_CONFIDENCE = 0.4
    
    # Hybrid System Configuration
    USE_GEMINI_ENHANCEMENT = True  # Enable Gemini enhancement
    GEMINI_ENHANCEMENT_THRESHOLD = 0.5  # Only use Gemini if ML confidence is below this
    MAX_GEMINI_RETRIES = 2
    GEMINI_TIMEOUT = 10  # seconds
    
    # Safety Configuration
    ENABLE_EMERGENCY_DETECTION = True
    EMERGENCY_BYPASS_ML = True  # Emergency detection bypasses all other processing
    
    # Logging Configuration
    LOG_LEVEL = "INFO"
    LOG_GEMINI_REQUESTS = False  # Set to True for debugging (be careful with sensitive data)
    
    @classmethod
    def is_gemini_available(cls) -> bool:
        """Check if Gemini API is available and configured"""
        return cls.GEMINI_API_KEY is not None and len(cls.GEMINI_API_KEY.strip()) > 0
    
    @classmethod
    def get_gemini_url(cls) -> str:
        """Get the full Gemini API URL"""
        return cls.GEMINI_API_URL.format(model=cls.GEMINI_MODEL)
