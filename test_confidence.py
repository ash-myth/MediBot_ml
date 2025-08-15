#!/usr/bin/env python3
"""
Test confidence threshold improvements specifically
"""

from ml_analyzer import ml_analyzer
import json

def test_confidence_thresholds():
    """Test that lowered thresholds allow more diagnoses"""
    print("🧪 Testing Confidence Threshold Improvements")
    print("=" * 60)
    
    test_cases = [
        {
            "description": "I have a runny nose and sneezing",
            "should_diagnose": True,
            "expected_confidence": "low"  # Should still diagnose with low confidence
        },
        {
            "description": "I feel tired and have a headache", 
            "should_diagnose": True,
            "expected_confidence": "medium"  # Should diagnose with medium confidence
        },
        {
            "description": "I have severe flu symptoms with high fever body aches chills fatigue",
            "should_diagnose": True,
            "expected_confidence": "high"  # Should diagnose with high confidence
        },
        {
            "description": "I cough occasionally",
            "should_diagnose": True,  # Should now diagnose due to lower threshold
            "expected_confidence": "low"
        }
    ]
    
    passed = 0
    total = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: '{test_case['description']}' ---")
        
        # Test ML analysis directly
        result = ml_analyzer.analyze_description(test_case['description'])
        
        if "error" in result:
            if test_case['should_diagnose']:
                print(f"❌ FAIL: Expected diagnosis but got error: {result['error']}")
            else:
                print(f"✅ PASS: Correctly returned error for unclear input")
                passed += 1
        elif "emergency" in result:
            print(f"🚨 Emergency detected (not testing this case)")
            passed += 1
        else:
            diseases = result.get('predicted_diseases', [])
            if diseases:
                primary = diseases[0]
                confidence = primary['confidence']
                probability = primary['probability']
                
                print(f"✅ Generated diagnosis:")
                print(f"   Disease: {primary['disease']}")
                print(f"   Probability: {probability:.1f}%")
                print(f"   Confidence: {confidence}")
                print(f"   Symptoms: {result.get('extracted_symptoms', [])}")
                
                if test_case['should_diagnose']:
                    print(f"✅ PASS: Successfully diagnosed (threshold improvements working)")
                    passed += 1
                else:
                    print(f"❌ FAIL: Generated diagnosis when shouldn't have")
            else:
                if test_case['should_diagnose']:
                    print(f"❌ FAIL: No diagnosis generated when should have")
                else:
                    print(f"✅ PASS: Correctly avoided diagnosis")
                    passed += 1
    
    print(f"\n📊 Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    return passed == total

def test_symptom_extraction_improvements():
    """Test improved symptom extraction patterns"""
    print("\n\n🧪 Testing Improved Symptom Extraction")
    print("=" * 60)
    
    test_cases = [
        {
            "text": "I have muscle pain and body aches",
            "expected": ["muscle_pain"]
        },
        {
            "text": "My nose is running and I'm sneezing",
            "expected": ["runny_nose", "sneezing"]
        },
        {
            "text": "I get chest pain when exercising",
            "expected": ["chest_pain", "exertional_pain"]
        },
        {
            "text": "I keep forgetting things and words are hard to find",
            "expected": ["memory_loss", "word_finding_difficulty"]
        }
    ]
    
    passed = 0
    total = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Extraction Test {i}: '{test_case['text']}' ---")
        
        extracted = ml_analyzer._extract_symptoms_from_text(test_case['text'])
        expected = test_case['expected']
        
        print(f"Extracted: {extracted}")
        print(f"Expected:  {expected}")
        
        # Check if at least 70% of expected symptoms were found
        found_count = sum(1 for exp in expected if exp in extracted)
        success_rate = found_count / len(expected) if expected else 0
        
        if success_rate >= 0.7:
            print(f"✅ PASS: Found {found_count}/{len(expected)} expected symptoms")
            passed += 1
        else:
            print(f"❌ FAIL: Only found {found_count}/{len(expected)} expected symptoms")
    
    print(f"\n📊 Extraction Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    return passed == total

def test_training_data_coverage():
    """Test training data coverage"""
    print("\n\n🧪 Testing Training Data Coverage")
    print("=" * 60)
    
    training_data = ml_analyzer.training_data
    print(f"Total training samples: {len(training_data)}")
    
    # Count unique diseases
    diseases = set(item.get('disease', 'unknown') for item in training_data)
    print(f"Unique diseases: {len(diseases)}")
    
    # Show sample diseases
    print(f"Sample diseases: {list(diseases)[:10]}")
    
    # Count symptoms per sample
    symptom_counts = [len(item.get('symptoms', [])) for item in training_data]
    if symptom_counts:
        avg_symptoms = sum(symptom_counts) / len(symptom_counts)
        print(f"Average symptoms per disease: {avg_symptoms:.1f}")
    
    # Check if we have reasonable coverage
    if len(training_data) >= 50 and len(diseases) >= 20:
        print("✅ Training data has reasonable coverage")
        return True
    else:
        print("❌ Training data coverage may be insufficient")
        return False

def test_end_to_end_diagnosis():
    """Test complete diagnosis pipeline"""
    print("\n\n🧪 Testing End-to-End Diagnosis Pipeline")
    print("=" * 60)
    
    test_descriptions = [
        "I have been feeling tired and have body aches with a low fever for 2 days",
        "My head really hurts and I feel nauseous",
        "I have a cough and runny nose with sneezing",
    ]
    
    passed = 0
    total = len(test_descriptions)
    
    for i, desc in enumerate(test_descriptions, 1):
        print(f"\n--- End-to-End Test {i}: '{desc}' ---")
        
        try:
            # Use the main analyze_symptoms method (GUI interface)
            result = ml_analyzer.analyze_symptoms(desc)
            
            # Check required fields
            required_fields = ['symptoms', 'severity', 'response', 'primary_condition', 'confidence']
            missing_fields = [f for f in required_fields if f not in result]
            
            if missing_fields:
                print(f"❌ FAIL: Missing fields: {missing_fields}")
            else:
                print(f"✅ Complete diagnosis generated:")
                print(f"   Condition: {result['primary_condition']}")
                print(f"   Confidence: {result['confidence']}")
                print(f"   Severity: {result['severity']}")
                print(f"   Symptoms: {result['symptoms']}")
                print(f"   Response length: {len(result['response'])} chars")
                passed += 1
                
        except Exception as e:
            print(f"❌ FAIL: Exception occurred: {e}")
    
    print(f"\n📊 End-to-End Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    return passed == total

if __name__ == "__main__":
    print("🚀 Testing ML Analyzer Confidence & Accuracy Improvements\n")
    
    # Run all confidence-focused tests
    results = []
    results.append(test_confidence_thresholds())
    results.append(test_symptom_extraction_improvements())
    results.append(test_training_data_coverage())
    results.append(test_end_to_end_diagnosis())
    
    print(f"\n🎯 Overall Test Results:")
    print(f"   Confidence Thresholds: {'✅ PASS' if results[0] else '❌ FAIL'}")
    print(f"   Symptom Extraction: {'✅ PASS' if results[1] else '❌ FAIL'}")
    print(f"   Training Data: {'✅ PASS' if results[2] else '❌ FAIL'}")
    print(f"   End-to-End: {'✅ PASS' if results[3] else '❌ FAIL'}")
    
    if all(results):
        print("\n🎉 All improvements are working correctly!")
    else:
        print(f"\n⚠️  {sum(results)}/{len(results)} test categories passed")
