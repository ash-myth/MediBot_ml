#!/usr/bin/env python3
"""
Demo: Automatic Disease Detection and Cure Recommendation
Shows how the app automatically detects flu and provides cure when user types detailed description
"""

from ml_analyzer import ml_analyzer

def demo_flu_detection():
    """Demo the exact flu description you provided"""
    
    print("🏥 ADVANCED SYMPTOM CHECKER DEMO")
    print("=" * 60)
    print("👤 USER INPUT:")
    print("-" * 40)
    
    flu_description = """When you have the flu, you might feel suddenly very unwell, almost like your whole body is protesting. You can get a high fever that makes you feel hot and shivery at the same time. Chills might make you wrap yourself in blankets even though your skin is burning. Your muscles and joints ache, so even simple movements feel heavy. Fatigue hits hard—you feel like you could sleep for a whole day and still not be rested. A cough and sore throat make talking or swallowing uncomfortable, and sometimes your head throbs as if someone is pressing on it. Everything feels overwhelming, and you mostly want to rest until your body fights it off."""
    
    print(f"'{flu_description}'")
    
    print("\n🤖 AI PROCESSING...")
    print("-" * 40)
    
    # Analyze the description
    result = ml_analyzer.analyze_symptoms(flu_description)
    
    # Show what the AI detected
    print("🔍 AUTOMATIC DETECTION RESULTS:")
    print(f"   • Symptoms Found: {', '.join(result['symptoms'])}")
    print(f"   • Disease Identified: {result.get('primary_condition', 'Unknown')}")
    print(f"   • Confidence: {result.get('confidence', 'Unknown').upper()}")
    print(f"   • Severity: {result['severity'].upper()}")
    
    print("\n💊 AUTOMATIC CURE & TREATMENT:")
    print("-" * 40)
    print(result['response'])
    
    print("\n" + "=" * 60)
    print("✅ RESULT: User types description → AI automatically finds disease + cure!")
    print("   No manual symptom selection needed!")

if __name__ == "__main__":
    demo_flu_detection()
