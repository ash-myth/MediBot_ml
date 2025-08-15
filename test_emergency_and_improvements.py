#!/usr/bin/env python3
"""
Comprehensive Test Suite for Emergency Detection and Accuracy Improvements
Tests the improvements made to fix accuracy and safety issues
"""

from ml_analyzer import ml_analyzer

def test_emergency_detection():
    """Test emergency symptom detection - most critical feature"""
    print("🚨 Testing Emergency Detection - Critical Safety Feature")
    print("=" * 70)
    
    emergency_test_cases = [
        {
            "description": "severe chest pain radiating to left arm with sweating and nausea",
            "expected_emergency": True,
            "test_name": "Heart Attack Symptoms"
        },
        {
            "description": "can't breathe properly gasping for air turning blue",
            "expected_emergency": True,
            "test_name": "Severe Breathing Emergency"
        },
        {
            "description": "worst headache of my life thunderclap sudden severe",
            "expected_emergency": True,
            "test_name": "Possible Stroke/Aneurysm"
        },
        {
            "description": "vomiting blood throwing up blood",
            "expected_emergency": True,
            "test_name": "Internal Bleeding"
        },
        {
            "description": "face drooping arm weakness speech slurred sudden confusion",
            "expected_emergency": True,
            "test_name": "Stroke Symptoms"
        },
        {
            "description": "I have a mild headache and feel a bit tired",
            "expected_emergency": False,
            "test_name": "Non-Emergency Symptoms"
        }
    ]
    
    emergency_tests_passed = 0
    total_emergency_tests = len(emergency_test_cases)
    
    for i, test_case in enumerate(emergency_test_cases, 1):
        print(f"\n🚨 Emergency Test {i}: {test_case['test_name']}")
        print(f"Input: '{test_case['description']}'")
        print("-" * 50)
        
        # Test emergency detection
        ml_results = ml_analyzer.analyze_description(test_case['description'])
        
        is_emergency = "emergency" in ml_results and ml_results["emergency"]
        expected = test_case['expected_emergency']
        
        if is_emergency == expected:
            status = "✅ PASS"
            emergency_tests_passed += 1
        else:
            status = "❌ FAIL"
        
        print(f"Expected Emergency: {expected}, Detected: {is_emergency} - {status}")
        
        if is_emergency:
            print("🚨 EMERGENCY RESPONSE:")
            print(ml_results.get("message", "No message")[:200] + "...")
    
    print("\n" + "=" * 70)
    print(f"Emergency Detection Results: {emergency_tests_passed}/{total_emergency_tests} tests passed")
    
    if emergency_tests_passed == total_emergency_tests:
        print("✅ ALL EMERGENCY TESTS PASSED - System is safe for emergency situations!")
    else:
        print("❌ EMERGENCY TESTS FAILED - CRITICAL SAFETY ISSUE!")
    
    return emergency_tests_passed == total_emergency_tests

def test_input_validation():
    """Test that invalid inputs are handled correctly"""
    print("\n🔧 Testing Input Validation - Preventing Wrong Diagnoses")
    print("=" * 70)
    
    invalid_input_cases = [
        {
            "input": "",
            "test_name": "Empty input"
        },
        {
            "input": "asdfgh qwerty nonsense",
            "test_name": "Nonsense text"
        },
        {
            "input": "a",
            "test_name": "Single character"
        },
        {
            "input": "hello how are you today",
            "test_name": "Social greeting without symptoms"
        }
    ]
    
    validation_tests_passed = 0
    total_validation_tests = len(invalid_input_cases)
    
    for i, test_case in enumerate(invalid_input_cases, 1):
        print(f"\n🔧 Validation Test {i}: {test_case['test_name']}")
        print(f"Input: '{test_case['input']}'")
        print("-" * 50)
        
        result = ml_analyzer.analyze_symptoms(test_case['input'])
        
        # Should not give medical diagnosis for invalid inputs
        has_medical_diagnosis = ("primary_condition" in result and 
                               result.get("confidence") != "unknown" and
                               result.get("symptoms", []) != [])
        
        if not has_medical_diagnosis:
            status = "✅ PASS - No inappropriate diagnosis"
            validation_tests_passed += 1
        else:
            status = "❌ FAIL - Gave medical diagnosis for invalid input"
        
        print(f"Response: {result.get('response', 'No response')[:100]}...")
        print(f"Status: {status}")
    
    print("\n" + "=" * 70)
    print(f"Input Validation Results: {validation_tests_passed}/{total_validation_tests} tests passed")
    
    return validation_tests_passed == total_validation_tests

def test_symptom_accuracy():
    """Test that symptom detection is more accurate"""
    print("\n🎯 Testing Symptom Detection Accuracy")
    print("=" * 70)
    
    accuracy_test_cases = [
        {
            "description": "I've been experiencing flu-like symptoms for two days including high fever, severe body aches, fatigue, and chills",
            "expected_symptoms": ["fever", "muscle_pain", "fatigue", "chills"],
            "test_name": "Complex flu description"
        },
        {
            "description": "Woke up with intense headache, feel very exhausted, and have been coughing all night with sore throat",
            "expected_symptoms": ["headache", "fatigue", "cough", "sore_throat"],
            "test_name": "Multiple clear symptoms"
        },
        {
            "description": "severe chest pain that spreads to my left arm with sweating",
            "expected_symptoms": ["chest_pain", "severe_chest_pain"],
            "test_name": "Emergency chest pain with radiation"
        }
    ]
    
    accuracy_tests_passed = 0
    total_accuracy_tests = len(accuracy_test_cases)
    
    for i, test_case in enumerate(accuracy_test_cases, 1):
        print(f"\n🎯 Accuracy Test {i}: {test_case['test_name']}")
        print(f"Input: '{test_case['description']}'")
        print("-" * 50)
        
        result = ml_analyzer.analyze_symptoms(test_case['description'])
        detected_symptoms = [s.lower().replace(' ', '_') for s in result.get('symptoms', [])]
        
        # Check how many expected symptoms were detected
        matches = 0
        for expected in test_case['expected_symptoms']:
            if any(expected.lower() in detected.lower() or detected.lower() in expected.lower() 
                   for detected in detected_symptoms):
                matches += 1
        
        accuracy = matches / len(test_case['expected_symptoms']) if test_case['expected_symptoms'] else 0
        
        if accuracy >= 0.5:  # At least 50% of symptoms detected
            status = "✅ PASS"
            accuracy_tests_passed += 1
        else:
            status = "❌ FAIL"
        
        print(f"Expected symptoms: {test_case['expected_symptoms']}")
        print(f"Detected symptoms: {detected_symptoms}")
        print(f"Accuracy: {accuracy:.1%} - {status}")
    
    print("\n" + "=" * 70)
    print(f"Symptom Detection Results: {accuracy_tests_passed}/{total_accuracy_tests} tests passed")
    
    return accuracy_tests_passed == total_accuracy_tests

def test_confidence_thresholds():
    """Test that the system acknowledges uncertainty appropriately"""
    print("\n🤔 Testing Confidence and Uncertainty Handling")
    print("=" * 70)
    
    confidence_test_cases = [
        {
            "description": "I feel a bit off today",
            "should_be_uncertain": True,
            "test_name": "Vague symptoms"
        },
        {
            "description": "maybe I have something",
            "should_be_uncertain": True,
            "test_name": "Very unclear description"
        },
        {
            "description": "I have high fever, severe body aches, chills, and fatigue for three days",
            "should_be_uncertain": False,
            "test_name": "Clear flu symptoms"
        }
    ]
    
    confidence_tests_passed = 0
    total_confidence_tests = len(confidence_test_cases)
    
    for i, test_case in enumerate(confidence_test_cases, 1):
        print(f"\n🤔 Confidence Test {i}: {test_case['test_name']}")
        print(f"Input: '{test_case['description']}'")
        print("-" * 50)
        
        result = ml_analyzer.analyze_symptoms(test_case['description'])
        
        # Check if system expresses appropriate uncertainty
        has_low_confidence = (
            result.get("confidence", "").lower() == "low" or
            "uncertain" in result.get("response", "").lower() or
            "not sure" in result.get("response", "").lower() or
            "more information" in result.get("response", "").lower() or
            "trouble analyzing" in result.get("response", "").lower()
        )
        
        expected_uncertainty = test_case['should_be_uncertain']
        
        if has_low_confidence == expected_uncertainty:
            status = "✅ PASS"
            confidence_tests_passed += 1
        else:
            status = "❌ FAIL"
        
        print(f"Expected uncertainty: {expected_uncertainty}, System uncertain: {has_low_confidence}")
        print(f"Confidence: {result.get('confidence', 'unknown')}")
        print(f"Status: {status}")
    
    print("\n" + "=" * 70)
    print(f"Confidence Handling Results: {confidence_tests_passed}/{total_confidence_tests} tests passed")
    
    return confidence_tests_passed == total_confidence_tests

def run_comprehensive_test_suite():
    """Run all tests and provide comprehensive safety assessment"""
    print("🧪 COMPREHENSIVE SAFETY AND ACCURACY TEST SUITE")
    print("=" * 70)
    print("Testing critical improvements to ensure system safety and accuracy")
    print("=" * 70)
    
    test_results = {}
    
    # Run all test categories
    test_results['emergency'] = test_emergency_detection()
    test_results['validation'] = test_input_validation() 
    test_results['accuracy'] = test_symptom_accuracy()
    test_results['confidence'] = test_confidence_thresholds()
    
    # Overall assessment
    print("\n" + "🏥 FINAL SAFETY AND ACCURACY ASSESSMENT" + "\n" + "=" * 70)
    
    passed_tests = sum(test_results.values())
    total_tests = len(test_results)
    
    print(f"Emergency Detection: {'✅ SAFE' if test_results['emergency'] else '❌ UNSAFE - CRITICAL ISSUE!'}")
    print(f"Input Validation: {'✅ PROTECTED' if test_results['validation'] else '❌ VULNERABLE'}")
    print(f"Symptom Accuracy: {'✅ ACCURATE' if test_results['accuracy'] else '❌ INACCURATE'}")
    print(f"Confidence Handling: {'✅ APPROPRIATE' if test_results['confidence'] else '❌ OVERCONFIDENT'}")
    
    print("\n" + "-" * 70)
    print(f"OVERALL SCORE: {passed_tests}/{total_tests} test categories passed")
    
    if test_results['emergency']:
        if passed_tests == total_tests:
            print("\n✅ SYSTEM IS READY FOR USE - All safety and accuracy tests passed!")
            print("The symptom checker is now safe for emergency situations and provides accurate assessments.")
        else:
            print("\n⚠️ SYSTEM HAS ISSUES - Emergency detection works but other areas need improvement.")
    else:
        print("\n🚨 SYSTEM IS NOT SAFE - Emergency detection failed!")
        print("DO NOT USE THIS SYSTEM until emergency detection is fixed!")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    try:
        # Run comprehensive test suite
        all_tests_passed = run_comprehensive_test_suite()
        
        if all_tests_passed:
            print("\n🎉 SUCCESS: All improvements are working correctly!")
            print("The symptom checker is now accurate and safe for emergency use.")
        else:
            print("\n⚠️ Some tests failed. Review the results above to identify issues.")
            
    except Exception as e:
        print(f"❌ Test suite failed with error: {e}")
        print("There may be critical issues with the system.")
