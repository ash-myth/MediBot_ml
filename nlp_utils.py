"""
Natural Language Processing Utilities
Advanced text processing for better symptom understanding and conversation flow
"""

import re
import json
from typing import Dict, List, Tuple, Set
from fuzzywuzzy import fuzz, process
from datetime import datetime, timedelta
from collections import defaultdict

class SymptomNLP:
    def __init__(self):
        # Symptom synonyms and related terms
        self.symptom_synonyms = {
            "headache": ["head pain", "migraine", "head ache", "cranial pain", "cephalgia"],
            "nausea": ["sick feeling", "queasy", "upset stomach", "feeling sick", "nauseated"],
            "fever": ["high temperature", "pyrexia", "febrile", "hot", "burning up", "temperature"],
            "cough": ["coughing", "hacking", "dry cough", "wet cough", "productive cough"],
            "fatigue": ["tired", "exhausted", "weakness", "lethargic", "worn out", "drained"],
            "dizziness": ["dizzy", "lightheaded", "vertigo", "spinning", "unsteady", "wobbly"],
            "shortness_of_breath": ["can't breathe", "breathing problems", "winded", "breathless", "dyspnea"],
            "chest_pain": ["chest ache", "heart pain", "chest tightness", "chest pressure"],
            "sore_throat": ["throat pain", "scratchy throat", "painful swallowing", "throat ache"],
            "abdominal_pain": ["stomach pain", "belly ache", "tummy ache", "stomach ache", "gut pain"],
            "joint_pain": ["arthritis", "joint ache", "stiff joints", "joint stiffness"],
            "muscle_pain": ["muscle ache", "sore muscles", "muscle soreness", "myalgia"],
            "rash": ["skin rash", "skin irritation", "red spots", "skin bumps", "dermatitis"],
            "vomiting": ["throwing up", "puking", "being sick", "emesis", "upchuck"],
            "diarrhea": ["loose stools", "runny stools", "frequent bowel movements", "loose bowels"]
        }
        
        # Severity indicators
        self.severity_indicators = {
            "mild": ["slight", "little", "minor", "barely", "light", "weak", "gentle"],
            "moderate": ["medium", "average", "normal", "regular", "okay", "moderate"],
            "severe": ["bad", "terrible", "awful", "intense", "extreme", "unbearable", "sharp", "strong", "heavy"]
        }
        
        # Time indicators
        self.time_patterns = {
            "duration": {
                "minutes": r"(\d+)\s*(?:min|minute|minutes)",
                "hours": r"(\d+)\s*(?:hr|hour|hours)",
                "days": r"(\d+)\s*(?:day|days)",
                "weeks": r"(\d+)\s*(?:week|weeks)",
                "months": r"(\d+)\s*(?:month|months)"
            },
            "frequency": {
                "daily": ["every day", "daily", "each day"],
                "hourly": ["every hour", "hourly", "each hour"],
                "intermittent": ["on and off", "sometimes", "occasionally", "intermittent"]
            }
        }
        
        # Question patterns for better understanding
        self.question_patterns = {
            "location": ["where", "which part", "location", "area"],
            "duration": ["how long", "since when", "duration", "started"],
            "severity": ["how bad", "how severe", "intensity", "scale"],
            "frequency": ["how often", "frequency", "regular", "pattern"],
            "triggers": ["what makes", "triggers", "causes", "brings on"],
            "relief": ["what helps", "relieves", "makes better", "improves"]
        }
        
        # Emotional indicators
        self.emotional_indicators = {
            "worried": ["worried", "concerned", "anxious", "scared", "frightened"],
            "frustrated": ["frustrated", "annoyed", "irritated", "fed up"],
            "confused": ["confused", "don't understand", "unclear", "puzzled"],
            "urgent": ["urgent", "emergency", "immediate", "help", "serious"]
        }
    
    def extract_symptoms_from_text(self, text: str) -> List[Tuple[str, float]]:
        """Extract symptoms from user text using fuzzy matching"""
        text_lower = text.lower()
        detected_symptoms = []
        
        # Direct symptom matching
        for symptom, synonyms in self.symptom_synonyms.items():
            all_terms = [symptom.replace("_", " ")] + synonyms
            
            for term in all_terms:
                if term in text_lower:
                    confidence = 0.9 if term == symptom.replace("_", " ") else 0.7
                    detected_symptoms.append((symptom, confidence))
                    break
        
        # Fuzzy matching for partial matches
        words = text_lower.split()
        for word in words:
            if len(word) > 3:  # Only check longer words
                for symptom in self.symptom_synonyms.keys():
                    symptom_words = symptom.replace("_", " ").split()
                    for symptom_word in symptom_words:
                        ratio = fuzz.ratio(word, symptom_word)
                        if ratio > 80:  # High similarity threshold
                            detected_symptoms.append((symptom, ratio / 100))
        
        # Remove duplicates and sort by confidence
        unique_symptoms = {}
        for symptom, confidence in detected_symptoms:
            if symptom not in unique_symptoms or confidence > unique_symptoms[symptom]:
                unique_symptoms[symptom] = confidence
        
        return sorted(unique_symptoms.items(), key=lambda x: x[1], reverse=True)
    
    def extract_severity(self, text: str) -> str:
        """Extract severity level from text"""
        text_lower = text.lower()
        
        # Check for explicit severity mentions
        for severity, indicators in self.severity_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    return severity
        
        # Check for numeric scales (1-10)
        scale_match = re.search(r'(?:rate|scale|level).*?(\d+)(?:\s*(?:out of|/)?\s*10)?', text_lower)
        if scale_match:
            scale_value = int(scale_match.group(1))
            if scale_value <= 3:
                return "mild"
            elif scale_value <= 7:
                return "moderate"
            else:
                return "severe"
        
        return "moderate"  # Default
    
    def extract_duration(self, text: str) -> Dict[str, int]:
        """Extract duration information from text"""
        duration_info = {}
        
        for unit, pattern in self.time_patterns["duration"].items():
            matches = re.findall(pattern, text.lower())
            if matches:
                duration_info[unit] = int(matches[0])
        
        return duration_info
    
    def extract_frequency(self, text: str) -> str:
        """Extract frequency information from text"""
        text_lower = text.lower()
        
        for freq_type, indicators in self.time_patterns["frequency"].items():
            for indicator in indicators:
                if indicator in text_lower:
                    return freq_type
        
        return "unknown"
    
    def analyze_emotional_state(self, text: str) -> List[str]:
        """Analyze emotional indicators in user text"""
        text_lower = text.lower()
        emotions = []
        
        for emotion, indicators in self.emotional_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    emotions.append(emotion)
                    break
        
        return emotions
    
    def generate_follow_up_question(self, symptom: str, context: Dict) -> str:
        """Generate intelligent follow-up questions based on context"""
        base_questions = {
            "headache": [
                "Is the headache throbbing or more like pressure?",
                "Where exactly is the headache located?",
                "Does light or sound make it worse?",
                "Have you experienced any vision changes?"
            ],
            "chest_pain": [
                "Is the chest pain sharp or crushing?",
                "Does it radiate to your arm, jaw, or back?",
                "Does it worsen with deep breathing or movement?",
                "Are you experiencing any shortness of breath with it?"
            ],
            "fever": [
                "Do you know your current temperature?",
                "Are you experiencing chills or sweating?",
                "How long have you had the fever?",
                "Have you taken any fever-reducing medication?"
            ],
            "nausea": [
                "Have you actually vomited or just feel nauseous?",
                "Is it related to eating or drinking anything?",
                "Are you experiencing any stomach pain with it?",
                "Does movement make it worse?"
            ]
        }
        
        questions = base_questions.get(symptom, [
            f"Can you describe the {symptom.replace('_', ' ')} in more detail?",
            f"How long have you been experiencing {symptom.replace('_', ' ')}?",
            f"On a scale of 1-10, how would you rate the {symptom.replace('_', ' ')}?"
        ])
        
        # Select question based on context
        asked_questions = context.get('asked_questions', [])
        available_questions = [q for q in questions if q not in asked_questions]
        
        if available_questions:
            return available_questions[0]
        else:
            return f"Is there anything else about your {symptom.replace('_', ' ')} you'd like to mention?"
    
    def parse_response_to_question(self, response: str, question_type: str) -> Dict:
        """Parse user response to specific question types"""
        response_lower = response.lower()
        parsed_info = {"type": question_type, "raw_response": response}
        
        if question_type == "location":
            # Extract body parts/locations
            body_parts = ["head", "chest", "stomach", "back", "arm", "leg", "throat", "neck", "shoulder"]
            found_parts = [part for part in body_parts if part in response_lower]
            parsed_info["locations"] = found_parts
        
        elif question_type == "severity":
            parsed_info["severity"] = self.extract_severity(response)
            # Look for numeric ratings
            numbers = re.findall(r'\b(\d+)\b', response)
            if numbers:
                parsed_info["numeric_rating"] = int(numbers[0])
        
        elif question_type == "duration":
            parsed_info["duration"] = self.extract_duration(response)
        
        elif question_type == "frequency":
            parsed_info["frequency"] = self.extract_frequency(response)
        
        elif question_type == "yes_no":
            yes_indicators = ["yes", "yeah", "yep", "definitely", "absolutely", "sure"]
            no_indicators = ["no", "nope", "not", "never", "none"]
            
            if any(indicator in response_lower for indicator in yes_indicators):
                parsed_info["answer"] = "yes"
            elif any(indicator in response_lower for indicator in no_indicators):
                parsed_info["answer"] = "no"
            else:
                parsed_info["answer"] = "unclear"
        
        return parsed_info
    
    def generate_empathetic_response(self, symptoms: List[str], emotions: List[str]) -> str:
        """Generate empathetic responses based on symptoms and emotions"""
        base_responses = [
            "I understand you're not feeling well.",
            "Thank you for sharing that information with me.",
            "I can see this is concerning for you."
        ]
        
        # Adjust response based on emotions
        if "worried" in emotions or "anxious" in emotions:
            base_responses.append("I can understand why you might be feeling worried about these symptoms.")
        
        if "frustrated" in emotions:
            base_responses.append("I can imagine this must be frustrating for you.")
        
        if "urgent" in emotions:
            base_responses.append("I can see this feels urgent to you.")
        
        # Adjust based on symptoms
        serious_symptoms = ["chest_pain", "shortness_of_breath", "severe_headache"]
        if any(symptom in serious_symptoms for symptom in symptoms):
            base_responses.append("These symptoms can certainly be concerning.")
        
        # Select appropriate response
        import random
        return random.choice(base_responses)
    
    def suggest_clarifying_questions(self, symptoms: List[str], conversation_history: List[Dict]) -> List[str]:
        """Suggest clarifying questions based on symptoms and conversation"""
        questions = []
        asked_about = set()
        
        # Extract what's already been asked about
        for entry in conversation_history:
            if entry.get('type') == 'question':
                asked_about.add(entry.get('topic', ''))
        
        for symptom in symptoms:
            if f"{symptom}_duration" not in asked_about:
                questions.append(f"How long have you been experiencing {symptom.replace('_', ' ')}?")
            
            if f"{symptom}_severity" not in asked_about:
                questions.append(f"How severe is your {symptom.replace('_', ' ')} on a scale of 1-10?")
            
            if f"{symptom}_triggers" not in asked_about:
                questions.append(f"What seems to trigger or worsen your {symptom.replace('_', ' ')}?")
        
        return questions[:3]  # Return top 3 questions
    
    def extract_medical_history_info(self, text: str) -> Dict:
        """Extract relevant medical history information from text"""
        info = {
            "medications": [],
            "allergies": [],
            "conditions": [],
            "previous_episodes": False
        }
        
        text_lower = text.lower()
        
        # Common medication patterns
        med_patterns = [
            r"taking\s+(\w+)",
            r"on\s+(\w+)",
            r"medication\s+(\w+)",
            r"pills?\s+(\w+)"
        ]
        
        for pattern in med_patterns:
            matches = re.findall(pattern, text_lower)
            info["medications"].extend(matches)
        
        # Allergy patterns
        if "allergic" in text_lower or "allergy" in text_lower:
            allergy_match = re.search(r"allergic to (\w+)", text_lower)
            if allergy_match:
                info["allergies"].append(allergy_match.group(1))
        
        # Previous episodes
        previous_indicators = ["before", "previously", "had this", "experienced this"]
        if any(indicator in text_lower for indicator in previous_indicators):
            info["previous_episodes"] = True
        
        return info
    
    def classify_urgency_level(self, symptoms: List[str], severity_scores: Dict[str, str]) -> str:
        """Classify urgency level based on symptoms and severity"""
        high_urgency_symptoms = [
            "chest_pain", "shortness_of_breath", "severe_headache", 
            "high_fever", "difficulty_breathing", "severe_abdominal_pain"
        ]
        
        moderate_urgency_symptoms = [
            "fever", "persistent_cough", "severe_nausea", "vomiting"
        ]
        
        # Check for high urgency
        for symptom in symptoms:
            if symptom in high_urgency_symptoms:
                if severity_scores.get(symptom, "mild") in ["severe", "extreme"]:
                    return "high"
        
        # Check for moderate urgency
        severe_count = sum(1 for s in symptoms if severity_scores.get(s, "mild") == "severe")
        if severe_count >= 2 or any(s in moderate_urgency_symptoms for s in symptoms):
            return "moderate"
        
        return "low"

# Create global NLP instance
nlp_processor = SymptomNLP()
