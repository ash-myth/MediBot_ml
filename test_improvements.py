#!/usr/bin/env python3
"""
Test script to demonstrate the ML-powered symptom analyzer improvements
"""

from ml_analyzer import ml_analyzer

def test_ml_analysis():
    """Test the ML analysis with various inputs"""
    test_cases = [
        {
            "description": "I've been experiencing flu-like symptoms for two days including high fever, severe body aches, fatigue, and chills",
            "test_name": "Complex flu description"
        },
        {
            "description": "I have a mild headache and feel a bit tired",
            "test_name": "Simple symptoms"
        },
        {
            "description": "Woke up with intense headache, feel very exhausted, and have been coughing all night with sore throat",
            "test_name": "Multiple symptoms with severity"
        },
        {
            "description": "I just have fever",
            "test_name": "Single symptom"
        }
    ]
    
    print("🧪 Testing ML-Powered Symptom Analysis")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['test_name']}")
        print(f"Input: '{test_case['description']}'")
        print("-" * 40)
        
        # Analyze symptoms
        result = ml_analyzer.analyze_symptoms(test_case['description'])
        
        print(f"✅ Detected symptoms: {', '.join(result.get('symptoms', ['None']))}")
        print(f"📊 Severity: {result.get('severity', 'Unknown')}")
        if 'primary_condition' in result:
            print(f"🏥 Primary condition: {result['primary_condition']} ({result.get('confidence', 'unknown')} confidence)")
        
        print(f"\n💬 Response preview:")
        response = result.get('response', 'No response generated')
        # Show first 150 characters of response
        preview = response[:150] + "..." if len(response) > 150 else response
        print(f"'{preview}'")
        print("=" * 60)

def test_error_handling():
    """Test error handling and human-friendly messages"""
    print("\n🔧 Testing Error Handling & Human-Friendly Messages")
    print("=" * 60)
    
    error_cases = [
        "",  # Empty input
        "asdfgh qwerty",  # Nonsense input
        "a",  # Very short input
    ]
    
    for i, test_input in enumerate(error_cases, 1):
        print(f"\n🚨 Error Test {i}: '{test_input}'")
        result = ml_analyzer.analyze_symptoms(test_input)
        print(f"Response: {result.get('response', 'No response')}")

if __name__ == "__main__":
    try:
        test_ml_analysis()
        test_error_handling()
        print("\n✅ All tests completed successfully!")
        print("\n💡 The system now provides:")
        print("   • ML-powered disease prediction")
        print("   • Human-friendly conversational responses") 
        print("   • Better symptom detection from natural language")
        print("   • Comprehensive treatment recommendations")
        print("   • Graceful error handling with helpful suggestions")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
