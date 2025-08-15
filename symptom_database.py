"""
Comprehensive Symptom Database for Medical Condition Assessment
This database contains symptoms and their associated conditions with severity levels.
"""

import json
from typing import Dict, List, Tuple
import pandas as pd

class SymptomDatabase:
    def __init__(self):
        self.symptoms_data = {
            # Respiratory Symptoms
            "cough": {
                "conditions": ["common_cold", "flu", "bronchitis", "pneumonia", "covid19", "asthma", "allergies"],
                "severity_weights": {"mild": 1, "moderate": 2, "severe": 3},
                "questions": ["Is it a dry cough or productive?", "How long have you had this cough?", "Does it worsen at night?"]
            },
            "fever": {
                "conditions": ["flu", "covid19", "pneumonia", "infection", "common_cold"],
                "severity_weights": {"mild": 2, "moderate": 3, "severe": 4},
                "questions": ["What is your temperature?", "How long have you had fever?", "Any chills or sweating?"]
            },
            "shortness_of_breath": {
                "conditions": ["asthma", "pneumonia", "covid19", "heart_disease", "anxiety"],
                "severity_weights": {"mild": 2, "moderate": 4, "severe": 5},
                "questions": ["Does it occur at rest or with activity?", "Any chest pain?", "How sudden was the onset?"]
            },
            "chest_pain": {
                "conditions": ["heart_disease", "pneumonia", "anxiety", "muscle_strain", "acid_reflux"],
                "severity_weights": {"mild": 2, "moderate": 4, "severe": 5},
                "questions": ["Is it sharp or crushing?", "Does it radiate to arm or jaw?", "Triggered by movement?"]
            },
            "sore_throat": {
                "conditions": ["common_cold", "flu", "strep_throat", "allergies"],
                "severity_weights": {"mild": 1, "moderate": 2, "severe": 3},
                "questions": ["Any difficulty swallowing?", "White patches on throat?", "Swollen lymph nodes?"]
            },
            
            # Gastrointestinal Symptoms
            "nausea": {
                "conditions": ["food_poisoning", "migraine", "pregnancy", "anxiety", "flu"],
                "severity_weights": {"mild": 1, "moderate": 2, "severe": 3},
                "questions": ["Any vomiting?", "Related to eating?", "Any abdominal pain?"]
            },
            "abdominal_pain": {
                "conditions": ["appendicitis", "food_poisoning", "ibs", "gastritis", "kidney_stones"],
                "severity_weights": {"mild": 2, "moderate": 3, "severe": 4},
                "questions": ["Where exactly is the pain?", "Sharp or cramping?", "Any nausea or vomiting?"]
            },
            "diarrhea": {
                "conditions": ["food_poisoning", "ibs", "infection", "anxiety"],
                "severity_weights": {"mild": 1, "moderate": 2, "severe": 3},
                "questions": ["How many times per day?", "Any blood or mucus?", "Recent travel or new foods?"]
            },
            "vomiting": {
                "conditions": ["food_poisoning", "migraine", "appendicitis", "pregnancy"],
                "severity_weights": {"mild": 2, "moderate": 3, "severe": 4},
                "questions": ["How frequent?", "Any blood in vomit?", "Associated with fever?"]
            },
            
            # Neurological Symptoms
            "headache": {
                "conditions": ["tension_headache", "migraine", "sinus_infection", "dehydration"],
                "severity_weights": {"mild": 1, "moderate": 2, "severe": 4},
                "questions": ["Throbbing or pressure-like?", "Location of pain?", "Any visual changes?"]
            },
            "dizziness": {
                "conditions": ["dehydration", "low_blood_pressure", "anxiety", "inner_ear_problem"],
                "severity_weights": {"mild": 1, "moderate": 2, "severe": 3},
                "questions": ["Room spinning or lightheaded?", "Standing up triggers it?", "Any hearing changes?"]
            },
            "fatigue": {
                "conditions": ["flu", "covid19", "depression", "anemia", "sleep_disorder"],
                "severity_weights": {"mild": 1, "moderate": 2, "severe": 3},
                "questions": ["How long feeling tired?", "Sleep quality?", "Any weight changes?"]
            },
            
            # Musculoskeletal Symptoms
            "joint_pain": {
                "conditions": ["arthritis", "flu", "injury", "autoimmune_disease"],
                "severity_weights": {"mild": 1, "moderate": 2, "severe": 3},
                "questions": ["Which joints?", "Morning stiffness?", "Any swelling?"]
            },
            "muscle_pain": {
                "conditions": ["flu", "exercise_strain", "fibromyalgia", "injury"],
                "severity_weights": {"mild": 1, "moderate": 2, "severe": 3},
                "questions": ["Specific muscles or general?", "Recent exercise?", "Any weakness?"]
            },
            
            # Skin Symptoms
            "rash": {
                "conditions": ["allergies", "eczema", "infection", "autoimmune_disease"],
                "severity_weights": {"mild": 1, "moderate": 2, "severe": 3},
                "questions": ["Where on body?", "Itchy or painful?", "Any new products used?"]
            },
            "itching": {
                "conditions": ["allergies", "eczema", "dry_skin", "infection"],
                "severity_weights": {"mild": 1, "moderate": 2, "severe": 2},
                "questions": ["Localized or widespread?", "Any visible rash?", "Worse at certain times?"]
            },
            "chills": {
                "conditions": ["flu", "covid19", "fever", "infection", "pneumonia"],
                "severity_weights": {"mild": 1, "moderate": 2, "severe": 3},
                "questions": ["Are you also feeling hot/feverish?", "How long have you had chills?", "Any sweating?"]
            }
        }
        
        self.conditions_info = {
            "common_cold": {
                "name": "Common Cold",
                "description": "Viral upper respiratory tract infection",
                "typical_symptoms": ["cough", "sore_throat", "runny_nose", "fatigue"],
                "severity": "mild",
                "recommendations": ["Rest", "Fluids", "Over-the-counter medications"]
            },
            "flu": {
                "name": "Influenza",
                "description": "Viral infection affecting respiratory system",
                "typical_symptoms": ["fever", "cough", "muscle_pain", "fatigue", "headache"],
                "severity": "moderate",
                "recommendations": ["Rest", "Fluids", "Antiviral medication if early", "See doctor if severe"]
            },
            "covid19": {
                "name": "COVID-19",
                "description": "Coronavirus disease",
                "typical_symptoms": ["fever", "cough", "shortness_of_breath", "fatigue", "loss_of_taste"],
                "severity": "variable",
                "recommendations": ["Isolate", "Monitor symptoms", "Seek medical care if breathing difficulties"]
            },
            "pneumonia": {
                "name": "Pneumonia",
                "description": "Lung infection causing inflammation",
                "typical_symptoms": ["cough", "fever", "chest_pain", "shortness_of_breath"],
                "severity": "serious",
                "recommendations": ["See doctor immediately", "Antibiotics may be needed", "Rest and fluids"]
            },
            "asthma": {
                "name": "Asthma",
                "description": "Chronic respiratory condition",
                "typical_symptoms": ["shortness_of_breath", "cough", "wheezing", "chest_tightness"],
                "severity": "manageable",
                "recommendations": ["Use inhaler", "Avoid triggers", "See doctor for management plan"]
            },
            "heart_disease": {
                "name": "Heart Disease",
                "description": "Cardiovascular condition",
                "typical_symptoms": ["chest_pain", "shortness_of_breath", "fatigue", "palpitations"],
                "severity": "serious",
                "recommendations": ["Seek immediate medical attention", "Call emergency if severe chest pain"]
            },
            "anxiety": {
                "name": "Anxiety Disorder",
                "description": "Mental health condition causing physical symptoms",
                "typical_symptoms": ["chest_pain", "shortness_of_breath", "dizziness", "nausea"],
                "severity": "manageable",
                "recommendations": ["Relaxation techniques", "Consider counseling", "Speak with healthcare provider"]
            },
            "migraine": {
                "name": "Migraine",
                "description": "Severe headache disorder",
                "typical_symptoms": ["headache", "nausea", "sensitivity_to_light", "visual_changes"],
                "severity": "moderate",
                "recommendations": ["Rest in dark room", "Pain medication", "Identify triggers"]
            },
            "food_poisoning": {
                "name": "Food Poisoning",
                "description": "Illness from contaminated food",
                "typical_symptoms": ["nausea", "vomiting", "diarrhea", "abdominal_pain"],
                "severity": "moderate",
                "recommendations": ["Stay hydrated", "Rest", "Seek medical care if severe dehydration"]
            }
        }

    def get_symptom_info(self, symptom: str) -> Dict:
        """Get information about a specific symptom"""
        return self.symptoms_data.get(symptom.lower(), {})
    
    def get_condition_info(self, condition: str) -> Dict:
        """Get information about a specific condition"""
        return self.conditions_info.get(condition.lower(), {})
    
    def get_all_symptoms(self) -> List[str]:
        """Get list of all available symptoms"""
        return list(self.symptoms_data.keys())
    
    def get_related_conditions(self, symptoms: List[str]) -> Dict[str, float]:
        """Calculate condition probabilities based on symptoms"""
        condition_scores = {}
        
        for symptom in symptoms:
            if symptom in self.symptoms_data:
                conditions = self.symptoms_data[symptom]["conditions"]
                for condition in conditions:
                    if condition not in condition_scores:
                        condition_scores[condition] = 0
                    condition_scores[condition] += 1
        
        # Normalize scores
        total_symptoms = len(symptoms)
        for condition in condition_scores:
            condition_scores[condition] = (condition_scores[condition] / total_symptoms) * 100
        
        return dict(sorted(condition_scores.items(), key=lambda x: x[1], reverse=True))
    
    def get_follow_up_questions(self, symptom: str) -> List[str]:
        """Get follow-up questions for a symptom"""
        symptom_info = self.get_symptom_info(symptom)
        return symptom_info.get("questions", [])
    
    def calculate_severity_score(self, symptoms_with_severity: Dict[str, str]) -> int:
        """Calculate overall severity score based on symptoms and their severity levels"""
        total_score = 0
        for symptom, severity in symptoms_with_severity.items():
            if symptom in self.symptoms_data:
                weights = self.symptoms_data[symptom]["severity_weights"]
                total_score += weights.get(severity, 1)
        return total_score
    
    def get_emergency_symptoms(self) -> List[str]:
        """Get list of symptoms that might require emergency attention"""
        emergency_symptoms = []
        for symptom, data in self.symptoms_data.items():
            max_severity = max(data["severity_weights"].values())
            if max_severity >= 4:
                emergency_symptoms.append(symptom)
        return emergency_symptoms

# Create global instance
symptom_db = SymptomDatabase()
