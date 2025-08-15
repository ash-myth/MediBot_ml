"""
Advanced ML-Powered Symptom Analyzer
Uses machine learning models for intelligent medical symptom assessment
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import json
import re
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import os
import traceback
import requests
import asyncio
import time
from config import Config
from medical_database import medical_db

class MLSymptomAnalyzer:
    def __init__(self):
        self.symptom_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.disease_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.severity_classifier = RandomForestClassifier(n_estimators=50, random_state=42)
        self.label_encoder = LabelEncoder()
        
        # Enhanced symptom-disease training data
        self.training_data = self._create_enhanced_training_data()
        
        # Medical knowledge base
        self.medical_knowledge = self._load_medical_knowledge()
        
        # Train the models
        self._train_models()
        
        # Initialize Gemini integration
        self.config = Config()
    
    def _create_enhanced_training_data(self):
        """Load comprehensive training data from medical database with 1000+ diseases"""
        print("🏥 Loading comprehensive training data from medical database...")
        
        try:
            # Get training data from comprehensive medical database
            db_training_data = medical_db.get_training_data_for_ml()
            
            if db_training_data and len(db_training_data) > 0:
                print(f"✅ Loaded {len(db_training_data)} training samples from database")
                return db_training_data
            else:
                print("⚠️ No database training data found, using fallback data")
                return self._get_fallback_training_data()
                
        except Exception as e:
            print(f"❌ Error loading database training data: {e}")
            print("🔄 Using fallback training data")
            return self._get_fallback_training_data()
    
    def _get_fallback_training_data(self):
        """Fallback training data if database is unavailable"""
        return [
            # Basic fallback diseases
            {
                "description": "runny nose sneezing cough sore throat stuffy nose congestion",
                "symptoms": ["runny_nose", "sneezing", "cough", "sore_throat", "congestion"],
                "disease": "common_cold",
                "severity": "mild"
            },
            {
                "description": "sudden onset fever chills body aches fatigue headache cough sore throat muscle pain",
                "symptoms": ["fever", "chills", "muscle_pain", "fatigue", "headache", "cough", "sore_throat"],
                "disease": "influenza_a",
                "severity": "moderate"
            },
            {
                "description": "severe headache throbbing pain nausea sensitivity light sound",
                "symptoms": ["headache", "nausea", "photophobia"],
                "disease": "migraine_without_aura",
                "severity": "severe"
            },
            {
                "description": "chest pain when exercising walking upstairs exertion tight pressure",
                "symptoms": ["chest_pain", "dyspnea_on_exertion"],
                "disease": "angina_pectoris___stable",
                "severity": "moderate"
            },
            {
                "description": "anxious worried heart racing panic sweating nervous scared",
                "symptoms": ["anxiety", "palpitations", "sweating"],
                "disease": "anxiety",
                "severity": "moderate"
            }
        ]
    
    def _load_medical_knowledge(self):
        """Load comprehensive medical knowledge base"""
        return {
            "influenza": {
                "name": "Influenza (Flu)",
                "description": "A viral respiratory illness that can cause mild to severe illness",
                "common_symptoms": ["fever", "chills", "muscle_pain", "fatigue", "headache", "cough", "sore_throat"],
                "treatment": [
                    "Rest and get plenty of sleep",
                    "Drink lots of fluids (water, warm broths, tea)",
                    "Take over-the-counter pain relievers (acetaminophen, ibuprofen)",
                    "Antiviral medications if prescribed within 48 hours",
                    "Use a humidifier or breathe steam",
                    "Gargle with warm salt water for sore throat"
                ],
                "home_remedies": [
                    "Chicken soup for hydration and comfort",
                    "Honey and lemon tea for cough relief",
                    "Warm compress for aches",
                    "Extra rest and sleep"
                ],
                "when_to_see_doctor": [
                    "Difficulty breathing or shortness of breath",
                    "High fever (over 103°F/39.4°C)",
                    "Symptoms that improve then worsen",
                    "Dehydration signs",
                    "If you're in a high-risk group"
                ],
                "prevention": [
                    "Annual flu vaccination",
                    "Wash hands frequently",
                    "Avoid close contact with sick people",
                    "Cover coughs and sneezes"
                ]
            },
            "covid19": {
                "name": "COVID-19",
                "description": "A respiratory illness caused by the SARS-CoV-2 virus",
                "common_symptoms": ["fever", "cough", "shortness_of_breath", "fatigue", "muscle_pain", "loss_of_taste"],
                "treatment": [
                    "Isolate to prevent spread",
                    "Rest and stay hydrated",
                    "Monitor oxygen levels if possible",
                    "Take fever reducers as needed",
                    "Contact healthcare provider for guidance"
                ],
                "when_to_see_doctor": [
                    "Difficulty breathing",
                    "Persistent chest pain",
                    "Confusion or inability to stay awake",
                    "Bluish lips or face"
                ]
            },
            "common_cold": {
                "name": "Common Cold",
                "description": "A mild viral upper respiratory tract infection",
                "common_symptoms": ["runny_nose", "sneezing", "cough", "sore_throat", "mild_fever"],
                "treatment": [
                    "Get plenty of rest",
                    "Stay hydrated with water and warm liquids",
                    "Use saline nasal drops",
                    "Try throat lozenges",
                    "Use a humidifier"
                ],
                "home_remedies": [
                    "Warm salt water gargle",
                    "Honey for cough (not for children under 1 year)",
                    "Steam inhalation",
                    "Warm chicken soup"
                ]
            },
            "pneumonia": {
                "name": "Pneumonia",
                "description": "An infection that inflames air sacs in one or both lungs",
                "common_symptoms": ["cough", "fever", "chest_pain", "shortness_of_breath", "chills"],
                "treatment": [
                    "Seek immediate medical attention",
                    "Antibiotics if bacterial",
                    "Rest and fluids",
                    "Oxygen therapy if needed"
                ],
                "when_to_see_doctor": [
                    "Immediate medical attention required",
                    "Call doctor immediately for suspected pneumonia"
                ]
            },
            "angina": {
                "name": "Possible Angina (Heart-related chest discomfort)",
                "description": "Chest discomfort or tightness that occurs with exertion and may spread to the arms, neck, or jaw. It can be a sign of reduced blood flow to the heart.",
                "common_symptoms": ["chest_pain", "shortness_of_breath", "fatigue"],
                "treatment": [
                    "Stop activity and rest immediately",
                    "If prescribed, take nitroglycerin as directed by your doctor",
                    "Avoid strenuous activity until evaluated by a clinician",
                    "Manage risk factors (blood pressure, cholesterol, diabetes) with medical guidance"
                ],
                "when_to_see_doctor": [
                    "Call emergency services if chest pain lasts more than a few minutes or is severe",
                    "Chest discomfort with shortness of breath, sweating, nausea, or radiation to arm/neck/jaw",
                    "New or worsening chest pain with exertion"
                ],
                "prevention": [
                    "Regular check-ups and heart health screening",
                    "Quit smoking, maintain healthy diet, and exercise as advised by your doctor"
                ]
            },
            "mild_cognitive_impairment": {
                "name": "Possible Mild Cognitive Impairment",
                "description": "Gradual changes in memory, planning, and word-finding that are more than expected with normal aging but not severe enough to significantly impact daily independence.",
                "common_symptoms": ["memory_loss", "word_finding_difficulty", "attention_issues", "planning_difficulty"],
                "treatment": [
                    "Schedule an appointment with a healthcare provider for cognitive evaluation",
                    "Review medications that may affect memory",
                    "Screen for reversible causes (thyroid, B12 deficiency, sleep issues, depression)",
                    "Use memory aids (notes, reminders) and maintain routines",
                    "Regular physical activity and social engagement"
                ],
                "when_to_see_doctor": [
                    "Memory problems worsening or impacting work/home safety",
                    "New confusion, getting lost in familiar places",
                    "Noticeable decline reported by family or coworkers"
                ],
                "prevention": [
                    "Manage blood pressure, sugar, and cholesterol",
                    "Stay mentally and socially active; maintain good sleep hygiene"
                ]
            }
        }
    
    def _train_models(self):
        """Train the ML models with the training data"""
        # Prepare training data
        descriptions = [item["description"] for item in self.training_data]
        diseases = [item["disease"] for item in self.training_data]
        severities = [item["severity"] for item in self.training_data]
        
        # Vectorize descriptions
        X = self.symptom_vectorizer.fit_transform(descriptions)
        
        # Encode diseases
        y_disease = self.label_encoder.fit_transform(diseases)
        
        # Train disease classifier
        self.disease_classifier.fit(X, y_disease)
        
        # Train severity classifier
        severity_encoder = LabelEncoder()
        y_severity = severity_encoder.fit_transform(severities)
        self.severity_classifier.fit(X, y_severity)
        
        # Store encoders
        self.severity_encoder = severity_encoder
        
        print("✅ ML models trained successfully!")
    
    def _adjust_with_heuristics(self, disease_probs: Dict[str, float], extracted_symptoms: List[str], text: str) -> Dict[str, float]:
        """Apply rule-based adjustments to probabilities based on clinical heuristics."""
        text_lower = text.lower()
        probs = disease_probs.copy()
        
        # Helper to safely adjust and clamp
        def add_prob(disease, delta):
            if disease in probs:
                probs[disease] = max(0.0, min(1.0, probs[disease] + delta))
        
        # Heuristic 1: SOB + productive cough -> pneumonia more likely, flu less likely
        productive_keywords = any(k in text_lower for k in ["phlegm", "mucus", "sputum", "bring up", "brings up", "productive cough"])
        sob_present = ("shortness_of_breath" in extracted_symptoms) or any(k in text_lower for k in ["breathing feels harder", "breathing harder", "breathing heavy", "winded", "harder than usual"]) 
        if ("cough" in extracted_symptoms or productive_keywords) and sob_present:
            add_prob("pneumonia", 0.15)
            add_prob("covid19", 0.05)
            add_prob("influenza", -0.10)
        
        # Heuristic 2: Worsening over time -> pneumonia more likely than flu (flu is acute)
        if any(phrase in text_lower for phrase in ["over time", "progressively", "worsen", "heavier over time", "getting worse"]):
            add_prob("pneumonia", 0.10)
            add_prob("influenza", -0.05)
        
        # Heuristic 3: No fever mentioned -> reduce influenza
        if "fever" not in extracted_symptoms and "fever" not in text_lower:
            add_prob("influenza", -0.10)
        
        # Heuristic 4: Exertional chest tightness +/- radiation -> angina more likely, anxiety less likely
        exertion = any(p in text_lower for p in ["doing things that require effort", "with effort", "when exercising", "when moving around", "climbing", "walking fast", "on exertion", "doing things that require"])
        chest_words = any(p in text_lower for p in ["chest feels funny", "chest feels \u201cfunny\u201d", "chest feels funny", "chest tight", "tight chest", "pressure in chest", "chest discomfort"]) or "chest_pain" in extracted_symptoms
        radiation = any(p in text_lower for p in ["spreads to your arms", "spreads to your arm", "to your neck", "to your jaw", "radiate to arm", "radiates to"])
        if chest_words and exertion:
            probs.setdefault("angina", 0.05)
            add_prob("angina", 0.25)
            add_prob("anxiety", -0.10)
        if chest_words and radiation:
            probs.setdefault("angina", 0.05)
            add_prob("angina", 0.25)
            add_prob("anxiety", -0.10)
        if exertion and "shortness_of_breath" in extracted_symptoms:
            probs.setdefault("angina", 0.05)
            add_prob("angina", 0.10)
            add_prob("anxiety", -0.05)
        
        # Heuristic 5: Cognitive decline patterns without infection -> favor MCI, reduce flu/infections
        cog_patterns = any(s in extracted_symptoms for s in ["memory_loss", "confusion", "word_finding_difficulty", "attention_issues", "planning_difficulty", "gradual_onset"])
        infection_markers = any(s in extracted_symptoms for s in ["fever", "cough", "chills"])
        if cog_patterns and not infection_markers:
            probs.setdefault("mild_cognitive_impairment", 0.05)
            add_prob("mild_cognitive_impairment", 0.35)
            add_prob("influenza", -0.20)
            add_prob("pneumonia", -0.10)
            add_prob("covid19", -0.10)
            # anxiety can still be considered but not primary
            add_prob("anxiety", 0.05)
        
        # Normalize to sum<=1 by scaling if needed
        total = sum(probs.values())
        if total > 1.0:
            for k in probs.keys():
                probs[k] = probs[k] / total
        return probs
    
    def analyze_description(self, description: str) -> Dict:
        """Analyze a natural language symptom description using ML"""
        # Input validation - check if input is valid before analysis
        if not description or len(description.strip()) < 5:
            return {
                "error": "insufficient_input",
                "message": "Please provide a more detailed description of your symptoms."
            }
        
        # Check if input contains actual symptom terms before processing
        description_lower = description.lower()
        symptom_terms = ["pain", "ache", "fever", "cough", "tired", "fatigue", "sick", 
                         "throat", "head", "nausea", "dizzy", "breathing", "chest", 
                         "stomach", "vomit", "diarrhea", "rash", "blood", "sweat", "chills"]
        
        # Check if any symptom term is in the description
        has_symptom_terms = any(term in description_lower for term in symptom_terms)
        if not has_symptom_terms and len(description.strip().split()) < 8:
            return {
                "error": "no_symptoms_detected",
                "message": "I couldn't detect any clear symptoms in your description. Please describe how you're feeling with specific symptoms."
            }
        
        try:
            # Vectorize the input description
            X = self.symptom_vectorizer.transform([description_lower])
            
            # Extract symptoms from description first - if none found in a reasonable length description,
            # we might not have enough medical info to proceed
            extracted_symptoms = self._extract_symptoms_from_text(description)
            
            # CRITICAL: Check for emergency symptoms first - this takes priority over everything else
            emergency_symptoms = self._check_for_emergency_symptoms(extracted_symptoms, description)
            if emergency_symptoms:
                return {
                    "emergency": True,
                    "emergency_symptoms": emergency_symptoms,
                    "message": self._generate_emergency_response(emergency_symptoms),
                    "extracted_symptoms": extracted_symptoms
                }
            
            if not extracted_symptoms and len(description.split()) > 10:
                return {
                    "error": "symptoms_unclear",
                    "message": "I couldn't identify specific symptoms from your description. Please mention specific symptoms like fever, cough, pain, etc.",
                    "extracted_symptoms": []
                }
            
            # Predict disease probabilities
            raw_probs = self.disease_classifier.predict_proba(X)[0]
            disease_classes = self.label_encoder.classes_
            disease_prob_map = {disease_classes[i]: float(raw_probs[i]) for i in range(len(disease_classes))}
            
            # Apply heuristic adjustments
            adjusted_probs = self._adjust_with_heuristics(disease_prob_map, extracted_symptoms, description)
            
            # Ensure angina considered if heuristics raised it significantly
            if adjusted_probs.get("angina", 0.0) > 0:
                pass  # already included
            
            # Build top predictions list - IMPROVED THRESHOLDS FOR BETTER ACCURACY
            top_items = sorted(adjusted_probs.items(), key=lambda x: x[1], reverse=True)[:3]
            predicted_diseases = []
            for disease, p in top_items:
                # LOWERED threshold for better coverage - was 0.15, now 0.08
                if p > 0.08:  # More reasonable threshold
                    predicted_diseases.append({
                        "disease": disease,
                        "probability": float(p * 100),
                        # IMPROVED confidence levels - more realistic thresholds
                        "confidence": "high" if p > 0.5 else "medium" if p > 0.2 else "low"
                    })
            
            # IMPROVED: Only reject if NO predictions or extremely low confidence
            if not predicted_diseases:
                return {
                    "error": "low_confidence",
                    "message": "I don't have enough information to make a confident assessment. Please provide more details about your symptoms.",
                    "extracted_symptoms": extracted_symptoms
                }
            
            # Predict severity
            severity_probs = self.severity_classifier.predict_proba(X)[0]
            severity_classes = self.severity_encoder.classes_
            predicted_severity = severity_classes[np.argmax(severity_probs)]
            severity_confidence = float(np.max(severity_probs))
            
            return {
                "predicted_diseases": predicted_diseases,
                "predicted_severity": predicted_severity,
                "severity_confidence": severity_confidence,
                "extracted_symptoms": extracted_symptoms,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error in ML analysis: {e}")
            return {"error": "processing_error", "message": "An error occurred while analyzing your symptoms. Please try again with a clearer description."}
    
    def _extract_symptoms_from_text(self, text: str) -> List[str]:
        """Extract symptoms from natural language text"""
        text_lower = text.lower()
        detected_symptoms = []
        
        # MASSIVELY ENHANCED symptom patterns with underscore and spaced variations
        symptom_patterns = {
            # Emergency symptoms - these require immediate attention
            "severe_chest_pain": [r"\bsevere.*chest.*pain\b", r"\bcrushing.*chest.*pain\b", r"\bchest.*crushing\b", r"\bchest.*pressure.*severe\b"],
            "chest_pain": [r"\bchest.*pain\b", r"\bchest.*hurt\b", r"\bchest.*ache\b", r"\bchest.*tight\b", r"\bchest.*pressure\b", r"\btight.*chest\b", r"\bpressure.*chest\b"],
            "severe_breathing": [r"\bcan't\s*breath(e)?\b", r"\bunable.*breath(e)?\b", r"\bgasping\b", r"\bsevere.*breath\b"],
            "shortness_of_breath": [r"\bshortness.*breath\b", r"\bdifficulty.*breathing\b", r"\bbreath(ing)?\s*(hard|harder|heavy)\b", r"\bwinded\b", r"\bdyspnea\b", r"\bshort.*breath\b"],
            "unconsciousness": [r"\bunconscious\b", r"\bpassed\s*out\b", r"\bfainted\b", r"\blost\s*consciousness\b"],
            "severe_bleeding": [r"\bsevere.*bleed\b", r"\bheavy.*bleed\b", r"\bblood.*everywhere\b", r"\bgushing.*blood\b"],
            "stroke_symptoms": [r"\bface.*droop\b", r"\barm.*weakness\b", r"\bspeech.*slurred\b", r"\bsudden.*confusion\b"],
            "allergic_reaction": [r"\ballergic.*reaction\b", r"\bswelling.*face\b", r"\btongue.*swell\b", r"\bhives\b", r"\banaphylax\b"],
            
            # NOSE & RESPIRATORY - MUCH EXPANDED WITH UNDERSCORES
            "runny_nose": [r"\brunny.*nose\b", r"\bnose.*running\b", r"\bnose.*dripping\b", r"\bnasal.*discharge\b", r"\bstuff.*running\b", r"\brunny nose\b"],
            "sneezing": [r"\bsneezing\b", r"\bsneeze\b", r"\bsneezes\b", r"\bsneezy\b", r"\bachoo\b"],
            "congestion": [r"\bstuff.*up\b", r"\bstuffs.*up\b", r"\bcongested\b", r"\bcongestion\b", r"\bnose.*blocked\b", r"\bblocked.*nose\b", r"\bcannot.*breathe.*nose\b", r"\bstuffy\b"],
            "itchy_eyes": [r"\bitchy.*eyes\b", r"\beyes.*itch\b", r"\bwatery.*eyes\b", r"\beyes.*watering\b", r"\beyes.*water\b"],
            
            # FEVER & CHILLS - EXPANDED
            "fever": [r"\bfever\b", r"\bhot\b", r"\bburning.*up\b", r"\btemperature\b", r"\bfebrile\b", r"\bfeverish\b", r"\bfeel.*hot\b", r"\bhigh.*temp\b"],
            "chills": [r"\bchills\b", r"\bshiver\b", r"\bshivering\b", r"\bcold\b", r"\bshaking\b", r"\bfreezing\b", r"\bgoosebumps\b"],
            
            # COUGH - MUCH EXPANDED  
            "cough": [r"\bcough\b", r"\bcoughing\b", r"\bhacking\b", r"\bbarking\b", r"\bdry.*cough\b", r"\bwet.*cough\b"],
            "productive_cough": [r"\b(phlegm|mucus|sputum)\b", r"\bbring.*up\b", r"\bbrings.*up\b", r"\bproductive.*cough\b", r"\bcough.*stuff.*up\b"],
            
            # THROAT - EXPANDED
            "sore_throat": [r"\bsore.*throat\b", r"\bthroat.*pain\b", r"\bthroat.*hurt\b", r"\bthroat.*ache\b", r"\bswallowing.*hurt\b", r"\bthroat.*scratchy\b", r"\bthroat.*raw\b"],
            
            # HEADACHE - MUCH EXPANDED
            "headache": [r"\bheadache\b", r"\bhead.*pain\b", r"\bhead.*hurt\b", r"\bhead.*ache\b", r"\bhead.*throb\b", r"\bmigraine\b", r"\bhead.*pounding\b", r"\bskull.*hurt\b", r"\bbad.*head\b", r"\bhead.*really.*hurt\b"],
            "severe_headache": [r"\bsevere.*headache\b", r"\bworst.*headache\b", r"\bheadache.*worst\b", r"\bthunder.*clap.*headache\b", r"\bhead.*killing.*me\b", r"\bexcruciating.*head\b"],
            
            # FATIGUE - MUCH EXPANDED
            "fatigue": [r"\bfatigue\b", r"\btired\b", r"\bexhausted\b", r"\bweakness\b", r"\bworn.*out\b", r"\bdrained\b", r"\bweak\b", r"\bno.*energy\b", r"\bfeel.*awful\b", r"\bwiped.*out\b"],
            
            # PAIN - MUCH EXPANDED
            "muscle_pain": [r"\bmuscle.*pain\b", r"\bmuscle.*ache\b", r"\bbody.*ache\b", r"\bbody.*pain\b", r"\bsore.*muscles\b", r"\baching.*all.*over\b", r"\bfeel.*sore\b"],
            "joint_pain": [r"\bjoint.*pain\b", r"\bjoint.*ache\b", r"\bstiff.*joints\b", r"\bjoint.*stiff\b"],
            "chest_pain": [r"\bchest.*pain\b", r"\bchest.*hurt\b", r"\bchest.*ache\b", r"\bchest.*tight\b", r"\bchest.*pressure\b", r"\bchest.*discomfort\b"],
            "abdominal_pain": [r"\bstomach.*pain\b", r"\babdominal.*pain\b", r"\bbelly.*ache\b", r"\bstomach.*ache\b", r"\bstomach.*hurt\b", r"\bstomach.*cramp\b"],
            "severe_abdominal_pain": [r"\bsevere.*stomach.*pain\b", r"\bsevere.*abdominal.*pain\b", r"\bstomach.*excruciating\b"],
            
            # NAUSEA & VOMITING - EXPANDED
            "nausea": [r"\bnausea\b", r"\bnauseous\b", r"\bsick\b", r"\bqueasy\b", r"\bfeel.*sick\b", r"\bwant.*throw.*up\b", r"\bstomach.*turning\b", r"\buneasy.*stomach\b"],
            "vomiting": [r"\bvomiting\b", r"\bthrow.*up\b", r"\bpuke\b", r"\bpuking\b", r"\bthrowing.*up\b", r"\bthrew.*up\b"],
            "vomiting_blood": [r"\bvomit.*blood\b", r"\bthrow.*up.*blood\b", r"\bblood.*vomit\b", r"\bhematemesis\b"],
            
            # DIGESTIVE - EXPANDED
            "diarrhea": [r"\bdiarrhea\b", r"\bloose.*stool\b", r"\brunny.*stool\b", r"\bwatery.*stool\b", r"\bfrequent.*bowel\b"],
            "bloody_stool": [r"\bblood.*stool\b", r"\bbloody.*stool\b", r"\bstool.*blood\b"],
            
            # NEUROLOGICAL - EXPANDED
            "dizziness": [r"\bdizzy\b", r"\bdizziness\b", r"\blightheaded\b", r"\bvertigo\b", r"\broom.*spinning\b", r"\bfeel.*unsteady\b"],
            "confusion": [r"\bconfus(ed|ing)?\b", r"\bfamiliar.*tasks\b", r"\bmixed.*up\b", r"\bdisoriented\b"],
            "memory_loss": [r"\bforget(ting)?\b", r"\bmemory\b", r"\bnames.*forget\b", r"\bforget.*small.*things\b", r"\bmemory.*problem\b", r"\bkeep.*forgetting\b"],
            "word_finding_difficulty": [r"\bword(s)?.*slip\b", r"\bfinding.*words\b", r"\bwords.*hard\b"],
            "attention_issues": [r"\bharder.*focus\b", r"\battention\b", r"\bconcentrat\b", r"\bfocus.*problem\b"],
            "planning_difficulty": [r"\bplan(ning)?.*hard\b", r"\bplan(ning)?.*difficult\b"],
            "gradual_onset": [r"\bgradual(ly)?\b", r"\bover.*time\b", r"\bnot.*right.*away\b"],
            
            # ANXIETY & PANIC - EXPANDED
            "anxiety": [r"\banxious\b", r"\banxiety\b", r"\bworried\b", r"\bpanic\b", r"\bscared\b", r"\bnervous\b", r"\bstressed\b", r"\bfeel.*anxious\b"],
            "heart_racing": [r"\bheart.*racing\b", r"\bheart.*pounding\b", r"\bpalpitations\b", r"\bheart.*fast\b", r"\bheart.*beating.*fast\b"],
            "sweating": [r"\bsweating\b", r"\bsweat\b", r"\bperspiring\b"],
            
            # EXERCISE/EXERTION - NEW (CRITICAL for angina detection)
            "exertional_pain": [r"\bwhen.*exercis\b", r"\bwhen.*walk\b", r"\bwhen.*climb\b", r"\bwith.*effort\b", r"\bwhen.*active\b", r"\bwhen.*moving\b", r"\bupstairs\b", r"\bexercise\b", r"\bexertion\b"],
            
            # SINUS - NEW
            "facial_pain": [r"\bfacial.*pain\b", r"\bsinus.*pressure\b", r"\bface.*pressure\b", r"\bsinus.*pain\b", r"\bface.*hurt\b"]
        }
        
        for symptom, patterns in symptom_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    if symptom not in detected_symptoms:
                        detected_symptoms.append(symptom)
                    break
        
        # Map productive_cough to cough if needed for downstream logic
        if "productive_cough" in detected_symptoms and "cough" not in detected_symptoms:
            detected_symptoms.append("cough")
        
        return detected_symptoms
    
    def _check_for_emergency_symptoms(self, extracted_symptoms: List[str], description: str) -> List[str]:
        """Check for emergency symptoms that require immediate medical attention"""
        emergency_symptoms = []
        
        # Define emergency symptoms
        critical_symptoms = {
            "severe_chest_pain": "Severe chest pain (possible heart attack)",
            "severe_breathing": "Severe breathing difficulties", 
            "unconsciousness": "Loss of consciousness",
            "severe_bleeding": "Severe bleeding",
            "stroke_symptoms": "Possible stroke symptoms",
            "allergic_reaction": "Severe allergic reaction",
            "vomiting_blood": "Vomiting blood",
            "bloody_stool": "Blood in stool",
            "severe_headache": "Severe sudden headache",
            "severe_abdominal_pain": "Severe abdominal pain"
        }
        
        # Check for emergency symptoms
        for symptom in extracted_symptoms:
            if symptom in critical_symptoms:
                emergency_symptoms.append(symptom)
        
        # Additional emergency checks based on combinations
        text_lower = description.lower()
        
        # Check for heart attack indicators
        chest_pain_present = any(s in extracted_symptoms for s in ["chest_pain", "severe_chest_pain"])
        heart_attack_keywords = any(phrase in text_lower for phrase in [
            "pain radiating to arm", "pain in left arm", "jaw pain", "sweating profusely", 
            "nausea with chest pain", "crushing pain", "elephant on chest"
        ])
        if chest_pain_present and heart_attack_keywords:
            if "severe_chest_pain" not in emergency_symptoms:
                emergency_symptoms.append("severe_chest_pain")
        
        # Check for severe breathing difficulties
        if any(phrase in text_lower for phrase in [
            "can't catch my breath", "gasping for air", "blue lips", "turning blue"
        ]):
            if "severe_breathing" not in emergency_symptoms:
                emergency_symptoms.append("severe_breathing")
        
        return emergency_symptoms
    
    def _generate_emergency_response(self, emergency_symptoms: List[str]) -> str:
        """Generate appropriate emergency response"""
        response = "🚨 EMERGENCY ALERT 🚨\n\n"
        response += "Based on your symptoms, this could be a medical emergency that requires IMMEDIATE attention.\n\n"
        
        if "severe_chest_pain" in emergency_symptoms:
            response += "🚨 CHEST PAIN EMERGENCY: Call 911 or emergency services immediately! This could be a heart attack.\n\n"
            response += "While waiting for help:\n"
            response += "• Sit down and try to stay calm\n"
            response += "• Chew an aspirin if you're not allergic\n"
            response += "• Loosen tight clothing\n"
            response += "• If you have nitroglycerin prescribed, take it\n\n"
        
        if "severe_breathing" in emergency_symptoms:
            response += "🚨 BREATHING EMERGENCY: Call 911 immediately! Severe breathing difficulties can be life-threatening.\n\n"
            response += "While waiting for help:\n"
            response += "• Sit upright\n"
            response += "• Try to stay calm\n"
            response += "• Use rescue inhaler if you have one\n\n"
        
        if "unconsciousness" in emergency_symptoms:
            response += "🚨 CONSCIOUSNESS EMERGENCY: If someone is unconscious, call 911 immediately!\n\n"
        
        if "severe_bleeding" in emergency_symptoms:
            response += "🚨 BLEEDING EMERGENCY: Call 911 for severe bleeding!\n\n"
            response += "While waiting for help:\n"
            response += "• Apply direct pressure to wound\n"
            response += "• Elevate injured area if possible\n"
            response += "• Do not remove embedded objects\n\n"
        
        if "stroke_symptoms" in emergency_symptoms:
            response += "🚨 POSSIBLE STROKE: Call 911 immediately! Remember F.A.S.T:\n"
            response += "• Face drooping\n"
            response += "• Arm weakness\n"
            response += "• Speech difficulty\n"
            response += "• Time to call emergency services\n\n"
        
        if "allergic_reaction" in emergency_symptoms:
            response += "🚨 ALLERGIC REACTION EMERGENCY: Call 911 for severe reactions!\n\n"
            response += "While waiting for help:\n"
            response += "• Use EpiPen if available\n"
            response += "• Remove or avoid the allergen\n"
            response += "• Lie flat with legs elevated if possible\n\n"
        
        if "vomiting_blood" in emergency_symptoms or "bloody_stool" in emergency_symptoms:
            response += "🚨 INTERNAL BLEEDING: Call 911 immediately! Blood in vomit or stool can indicate serious internal bleeding.\n\n"
        
        if "severe_headache" in emergency_symptoms:
            response += "🚨 SEVERE HEADACHE: Call 911 if this is the worst headache of your life! This could indicate a serious condition.\n\n"
        
        response += "📞 CALL EMERGENCY SERVICES NOW: \n"
        response += "• US: 911\n"
        response += "• UK: 999\n"
        response += "• EU: 112\n\n"
        
        response += "⚠️ DO NOT DELAY: These symptoms require immediate professional medical evaluation. "
        response += "This is not a time for home remedies or waiting. Get emergency medical help immediately.\n\n"
        
        response += "🚨 This assessment tool cannot replace emergency medical services. "
        response += "If you're experiencing these symptoms, stop using this app and call emergency services now!"
        
        return response
    
    def get_comprehensive_diagnosis(self, description: str) -> Dict:
        """Get comprehensive diagnosis with treatment recommendations"""
        # Run ML analysis
        ml_results = self.analyze_description(description)
        
        if "error" in ml_results:
            return ml_results
        
        # Get the most likely disease
        if ml_results["predicted_diseases"]:
            primary_disease = ml_results["predicted_diseases"][0]["disease"]
            disease_info = self.medical_knowledge.get(primary_disease, {})
            
            # Create comprehensive response
            diagnosis = {
                "primary_diagnosis": {
                    "condition": disease_info.get("name", primary_disease.replace("_", " ").title()),
                    "description": disease_info.get("description", ""),
                    "probability": ml_results["predicted_diseases"][0]["probability"],
                    "confidence": ml_results["predicted_diseases"][0]["confidence"]
                },
                "severity_assessment": {
                    "level": ml_results["predicted_severity"],
                    "confidence": ml_results["severity_confidence"]
                },
                "detected_symptoms": ml_results["extracted_symptoms"],
                "treatment_recommendations": disease_info.get("treatment", []),
                "home_remedies": disease_info.get("home_remedies", []),
                "when_to_see_doctor": disease_info.get("when_to_see_doctor", []),
                "prevention_tips": disease_info.get("prevention", []),
                "alternative_diagnoses": ml_results["predicted_diseases"][1:] if len(ml_results["predicted_diseases"]) > 1 else []
            }
            
            return diagnosis
        
        return {"error": "Could not determine diagnosis from description"}
    
    def generate_human_friendly_response(self, diagnosis: Dict) -> str:
        """Generate a human-friendly, conversational response based on ML diagnosis"""
        if "error" in diagnosis:
            return f"I'm sorry, I had trouble analyzing your symptoms: {diagnosis['error']}. Please try describing your symptoms differently or use simpler terms."
        
        primary = diagnosis["primary_diagnosis"]
        severity = diagnosis["severity_assessment"]
        
        # Start with empathetic opening
        response = f"I understand you're not feeling well. Based on your description, it sounds like you may have {primary['condition']}"
        
        # Add confidence level in human terms
        if primary['confidence'] == 'high':
            response += " (I'm quite confident about this assessment)"
        elif primary['confidence'] == 'medium':
            response += " (this seems likely based on your symptoms)"
        else:
            response += " (this is a possibility, but I'd recommend professional evaluation)"
        
        response += f".\n\n{primary['description']}"
        
        # Mention detected symptoms in a friendly way
        if diagnosis["detected_symptoms"]:
            symptoms_list = [s.replace("_", " ").title() for s in diagnosis["detected_symptoms"]]
            if len(symptoms_list) == 1:
                response += f"\n\nThe main symptom I noticed from your description is {symptoms_list[0]}."
            else:
                response += f"\n\nThe symptoms I identified include: {', '.join(symptoms_list[:-1])} and {symptoms_list[-1]}."
        
        # Severity assessment in plain language
        if severity['level'] == 'mild':
            response += " This appears to be a mild case, which is good news."
        elif severity['level'] == 'moderate':
            response += " This seems to be a moderate case that should be manageable with proper care."
        else:
            response += " This appears to be more severe and may require medical attention."
        
        # Treatment recommendations in a caring way
        if diagnosis["treatment_recommendations"]:
            response += "\n\nHere's what I recommend to help you feel better:"
            for i, treatment in enumerate(diagnosis["treatment_recommendations"], 1):
                response += f"\n{i}. {treatment}"
        
        # Home remedies with encouraging tone
        if diagnosis["home_remedies"]:
            response += "\n\nSome gentle home remedies that might provide comfort:"
            for remedy in diagnosis["home_remedies"]:
                response += f"\n• {remedy}"
        
        # Warning signs with appropriate urgency
        if diagnosis["when_to_see_doctor"]:
            response += "\n\nPlease seek medical attention if you experience any of these warning signs:"
            for warning in diagnosis["when_to_see_doctor"]:
                response += f"\n• {warning}"
        
        # Alternative possibilities
        if diagnosis["alternative_diagnoses"]:
            response += "\n\nOther conditions I considered:"
            for alt in diagnosis["alternative_diagnoses"]:
                response += f"\n• {alt['disease'].replace('_', ' ').title()} ({alt['probability']:.1f}% likelihood)"
        
        # Caring disclaimer
        response += "\n\nRemember, I'm here to provide information and support, but this assessment is not a substitute for professional medical advice. If you're concerned about your symptoms or they worsen, please don't hesitate to consult with a healthcare provider. I hope you feel better soon!"
        
        return response
    
    def _call_gemini_api(self, description: str, ml_diagnosis: Dict = None) -> Optional[Dict]:
        """Call Gemini API for enhanced diagnosis validation and improvement"""
        if not self.config.is_gemini_available() or not self.config.USE_GEMINI_ENHANCEMENT:
            return None
        
        try:
            # Prepare the prompt for Gemini
            prompt = self._create_gemini_prompt(description, ml_diagnosis)
            
            # Prepare the request
            headers = {
                'Content-Type': 'application/json',
            }
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.1,  # Low temperature for more consistent medical advice
                    "maxOutputTokens": 1000,
                    "topP": 0.8,
                    "topK": 40
                }
            }
            
            url = f"{self.config.get_gemini_url()}?key={self.config.GEMINI_API_KEY}"
            
            # Make the request with retry logic
            for attempt in range(self.config.MAX_GEMINI_RETRIES):
                try:
                    response = requests.post(
                        url, 
                        headers=headers, 
                        json=payload, 
                        timeout=self.config.GEMINI_TIMEOUT
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if 'candidates' in result and len(result['candidates']) > 0:
                            content = result['candidates'][0]['content']['parts'][0]['text']
                            return self._parse_gemini_response(content)
                    else:
                        print(f"Gemini API error {response.status_code}: {response.text}")
                        
                except requests.exceptions.RequestException as e:
                    print(f"Gemini API request failed (attempt {attempt + 1}): {e}")
                    if attempt < self.config.MAX_GEMINI_RETRIES - 1:
                        time.sleep(1)  # Brief delay before retry
                        
        except Exception as e:
            print(f"Unexpected error in Gemini API call: {e}")
            
        return None
    
    def _create_gemini_prompt(self, description: str, ml_diagnosis: Dict = None) -> str:
        """Create a structured prompt for Gemini to enhance diagnosis"""
        prompt = f"""You are a medical AI assistant helping to analyze symptoms. Please provide a structured medical assessment.

PATIENT DESCRIPTION:
{description}

ML INITIAL ANALYSIS:
{json.dumps(ml_diagnosis, indent=2) if ml_diagnosis else 'No ML analysis available'}

Please provide your assessment in this EXACT JSON format:
{{
    "primary_condition": "Most likely diagnosis",
    "confidence_level": "high/medium/low",
    "differential_diagnoses": [
        {{"condition": "Alternative diagnosis 1", "probability": 25}},
        {{"condition": "Alternative diagnosis 2", "probability": 15}}
    ],
    "key_symptoms": ["symptom1", "symptom2", "symptom3"],
    "severity": "mild/moderate/severe",
    "red_flags": ["warning sign 1", "warning sign 2"],
    "recommendations": [
        "Primary treatment recommendation",
        "Secondary treatment recommendation",
        "When to seek medical attention"
    ],
    "reasoning": "Brief explanation of diagnosis reasoning"
}}

IMPORTANT GUIDELINES:
- Be conservative and prioritize patient safety
- Always recommend professional medical evaluation for serious symptoms
- If symptoms suggest emergency, clearly state this
- Consider common conditions before rare ones
- Provide practical, evidence-based recommendations
- Response must be valid JSON only
"""
        return prompt
    
    def _parse_gemini_response(self, response_text: str) -> Optional[Dict]:
        """Parse and validate Gemini's JSON response"""
        try:
            # Try to extract JSON from the response
            response_text = response_text.strip()
            
            # Look for JSON block
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_text = response_text[start_idx:end_idx]
                parsed_response = json.loads(json_text)
                
                # Validate required fields
                required_fields = ['primary_condition', 'confidence_level', 'severity']
                if all(field in parsed_response for field in required_fields):
                    return parsed_response
                else:
                    print("Gemini response missing required fields")
            else:
                print("No valid JSON found in Gemini response")
                
        except json.JSONDecodeError as e:
            print(f"Failed to parse Gemini JSON response: {e}")
        except Exception as e:
            print(f"Error parsing Gemini response: {e}")
            
        return None
    
    def _merge_ml_and_gemini(self, ml_results: Dict, gemini_results: Dict, description: str) -> Dict:
        """Merge ML and Gemini results for enhanced accuracy"""
        try:
            # Start with ML results as base
            enhanced_results = ml_results.copy()
            
            # Extract confidence from both systems
            ml_confidence = ml_results.get('predicted_diseases', [{}])[0].get('probability', 0) / 100
            gemini_confidence_map = {'high': 0.9, 'medium': 0.6, 'low': 0.3}
            gemini_confidence = gemini_confidence_map.get(gemini_results.get('confidence_level', 'low'), 0.3)
            
            # If Gemini has higher confidence or detects different condition, consider enhancement
            if gemini_confidence > ml_confidence or gemini_results.get('primary_condition', '').lower() not in [d['disease'].lower() for d in ml_results.get('predicted_diseases', [])]:
                
                # Create enhanced prediction based on Gemini
                enhanced_disease = {
                    'disease': gemini_results['primary_condition'].lower().replace(' ', '_'),
                    'probability': gemini_confidence * 100,
                    'confidence': gemini_results['confidence_level']
                }
                
                # Update predicted diseases
                enhanced_results['predicted_diseases'] = [enhanced_disease] + ml_results.get('predicted_diseases', [])[:2]
                
                # Update severity if Gemini suggests different
                if gemini_results.get('severity') in ['mild', 'moderate', 'severe']:
                    enhanced_results['predicted_severity'] = gemini_results['severity']
                
                # Enhance extracted symptoms with Gemini's key symptoms
                gemini_symptoms = [s.lower().replace(' ', '_') for s in gemini_results.get('key_symptoms', [])]
                original_symptoms = enhanced_results.get('extracted_symptoms', [])
                enhanced_symptoms = list(set(original_symptoms + gemini_symptoms))
                enhanced_results['extracted_symptoms'] = enhanced_symptoms
                
                # Add Gemini reasoning
                enhanced_results['gemini_reasoning'] = gemini_results.get('reasoning', '')
                enhanced_results['enhanced_by_ai'] = True
            
            return enhanced_results
            
        except Exception as e:
            print(f"Error merging ML and Gemini results: {e}")
            return ml_results  # Fall back to ML results
    
    async def enhance_with_gemini(self, description: str, ml_results: Dict) -> Dict:
        """Enhance ML diagnosis with Gemini AI for improved accuracy"""
        try:
            # Skip Gemini enhancement for emergency cases
            if ml_results.get('emergency', False):
                return ml_results
            
            # Check if we should use Gemini enhancement
            if not self.config.USE_GEMINI_ENHANCEMENT or not self.config.is_gemini_available():
                return ml_results
            
            # Check ML confidence level - only enhance if below threshold
            ml_confidence = 0
            if ml_results.get('predicted_diseases'):
                ml_confidence = ml_results['predicted_diseases'][0].get('probability', 0) / 100
            
            if ml_confidence >= self.config.GEMINI_ENHANCEMENT_THRESHOLD:
                # ML is confident enough, no need for Gemini
                return ml_results
            
            # Call Gemini API
            gemini_results = self._call_gemini_api(description, ml_results)
            
            if gemini_results:
                # Merge results for enhanced accuracy
                enhanced_results = self._merge_ml_and_gemini(ml_results, gemini_results, description)
                return enhanced_results
            else:
                # Gemini failed, return original ML results
                return ml_results
                
        except Exception as e:
            print(f"Error in Gemini enhancement: {e}")
        return ml_results  # Always fall back to ML results
    
    def _create_diagnosis_from_results(self, results: Dict, description: str) -> Dict:
        """Create diagnosis structure from analysis results"""
        try:
            if "error" in results:
                return results
            
            # Get the most likely disease
            if results.get("predicted_diseases"):
                primary_disease = results["predicted_diseases"][0]["disease"]
                disease_info = self.medical_knowledge.get(primary_disease, {})
                
                # Create comprehensive diagnosis
                diagnosis = {
                    "primary_diagnosis": {
                        "condition": disease_info.get("name", primary_disease.replace("_", " ").title()),
                        "description": disease_info.get("description", ""),
                        "probability": results["predicted_diseases"][0]["probability"],
                        "confidence": results["predicted_diseases"][0]["confidence"]
                    },
                    "severity_assessment": {
                        "level": results.get("predicted_severity", "moderate"),
                        "confidence": results.get("severity_confidence", 0.5)
                    },
                    "detected_symptoms": results.get("extracted_symptoms", []),
                    "treatment_recommendations": disease_info.get("treatment", []),
                    "home_remedies": disease_info.get("home_remedies", []),
                    "when_to_see_doctor": disease_info.get("when_to_see_doctor", []),
                    "prevention_tips": disease_info.get("prevention", []),
                    "alternative_diagnoses": results["predicted_diseases"][1:] if len(results["predicted_diseases"]) > 1 else []
                }
                
                # Add Gemini reasoning if available
                if results.get('enhanced_by_ai') and results.get('gemini_reasoning'):
                    diagnosis['ai_reasoning'] = results['gemini_reasoning']
                
                return diagnosis
            
            return {"error": "Could not determine diagnosis from results"}
            
        except Exception as e:
            print(f"Error creating diagnosis from results: {e}")
            return {"error": "processing_error"}
    
    def generate_response_for_audience(self, diagnosis: Dict, audience: str = "Patient") -> str:
        """Return a response tailored for Patient or Clinician audiences."""
        if "error" in diagnosis:
            return self.generate_human_friendly_response(diagnosis)
        
        primary = diagnosis.get("primary_diagnosis", {})
        severity = diagnosis.get("severity_assessment", {})
        detected = [s.replace("_", " ").title() for s in diagnosis.get("detected_symptoms", [])]
        
        if audience == "Clinician":
            # Concise, structured handoff summary
            lines = []
            lines.append(f"Assessment: {primary.get('condition', 'Unknown')} ({primary.get('confidence','n/a')} confidence)")
            lines.append(f"Severity: {severity.get('level','moderate')} (p~{severity.get('confidence',0):.2f})")
            if detected:
                lines.append(f"Symptoms: {', '.join(detected)}")
            # Include alternative differentials if present
            alts = diagnosis.get("alternative_diagnoses", [])
            if alts:
                alt_text = ", ".join([f"{a['disease'].replace('_',' ').title()} ({a['probability']:.0f}%)" for a in alts])
                lines.append(f"Differentials: {alt_text}")
            # Recommendations succinct
            recs = diagnosis.get("treatment_recommendations", [])
            if recs:
                lines.append("Plan: " + "; ".join(recs[:4]))
            # Red flags
            warns = diagnosis.get("when_to_see_doctor", [])
            if warns:
                lines.append("Red flags: " + "; ".join(warns[:3]))
            return "\n".join(lines)
        else:
            # Patient-friendly narrative
            return self.generate_human_friendly_response(diagnosis)
    
    def analyze_symptoms(self, description: str) -> Dict:
        """Main method for analyzing symptoms - used by GUI with Gemini enhancement"""
        try:
            # First check for emergency conditions directly
            ml_results = self.analyze_description(description)
            
            # Handle emergency cases first - no Gemini needed for emergencies
            if "emergency" in ml_results and ml_results["emergency"]:
                return {
                    "symptoms": [s.replace("_", " ").title() for s in ml_results.get("extracted_symptoms", [])],
                    "severity": "severe",
                    "response": ml_results.get("message", "Emergency detected. Call 911 immediately."),
                    "primary_condition": "MEDICAL EMERGENCY",
                    "confidence": "emergency"
                }
            
            # Enhance ML results with Gemini if conditions are met
            try:
                enhanced_results = asyncio.run(self.enhance_with_gemini(description, ml_results))
                if enhanced_results.get('enhanced_by_ai', False):
                    print("✨ Diagnosis enhanced with AI")
            except Exception as gemini_error:
                print(f"Gemini enhancement failed, using ML only: {gemini_error}")
                enhanced_results = ml_results
            
            # Get comprehensive diagnosis from enhanced results
            if "error" in enhanced_results:
                # Try to enhance error handling with Gemini for unclear symptoms
                if self.config.is_gemini_available() and enhanced_results.get('error') in ['symptoms_unclear', 'low_confidence']:
                    try:
                        gemini_fallback = self._call_gemini_api(description)
                        if gemini_fallback:
                            return {
                                "symptoms": gemini_fallback.get('key_symptoms', []),
                                "severity": gemini_fallback.get('severity', 'moderate'),
                                "response": f"Based on your description, I think you might have {gemini_fallback.get('primary_condition', 'a condition that requires medical evaluation')}. {gemini_fallback.get('reasoning', '')} I recommend consulting with a healthcare provider for proper evaluation.",
                                "primary_condition": gemini_fallback.get('primary_condition', 'Unclear condition'),
                                "confidence": gemini_fallback.get('confidence_level', 'low')
                            }
                    except Exception as fallback_error:
                        print(f"Gemini fallback failed: {fallback_error}")
                
                return {
                    "symptoms": [],
                    "severity": "moderate",
                    "response": f"I'm sorry, I had trouble analyzing your symptoms. Please try describing them differently - for example, you might say 'I have fever and body aches' or 'I'm feeling tired with a headache'."
                }
            
            # Create diagnosis from enhanced results
            diagnosis = self._create_diagnosis_from_results(enhanced_results, description)
            
            if "error" in diagnosis:
                return {
                    "symptoms": [],
                    "severity": "moderate",
                    "response": "I'm having difficulty providing a confident assessment. Please describe your specific symptoms in more detail."
                }
            
            # Generate human-friendly response
            friendly_response = self.generate_human_friendly_response(diagnosis)
            
            # Return data in format expected by GUI
            return {
                "symptoms": [s.replace("_", " ").title() for s in diagnosis["detected_symptoms"]],
                "severity": diagnosis["severity_assessment"]["level"],
                "response": friendly_response,
                "primary_condition": diagnosis["primary_diagnosis"]["condition"],
                "confidence": diagnosis["primary_diagnosis"]["confidence"]
            }
            
        except Exception as e:
            print(f"Error in analyze_symptoms: {e}")
            return {
                "symptoms": [],
                "severity": "moderate", 
                "response": "I'm having some difficulty analyzing your symptoms right now. Could you try describing them in simpler terms? For example: 'I have a fever and headache' or 'I feel tired and nauseous'."
            }
    
    def save_model(self, filepath: str):
        """Save the trained models"""
        model_data = {
            'disease_classifier': self.disease_classifier,
            'severity_classifier': self.severity_classifier,
            'symptom_vectorizer': self.symptom_vectorizer,
            'label_encoder': self.label_encoder,
            'severity_encoder': self.severity_encoder
        }
        joblib.dump(model_data, filepath)
        print(f"✅ Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load pre-trained models"""
        try:
            model_data = joblib.load(filepath)
            self.disease_classifier = model_data['disease_classifier']
            self.severity_classifier = model_data['severity_classifier']
            self.symptom_vectorizer = model_data['symptom_vectorizer']
            self.label_encoder = model_data['label_encoder']
            self.severity_encoder = model_data['severity_encoder']
            print(f"✅ Model loaded from {filepath}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")

# Create global ML analyzer instance
ml_analyzer = MLSymptomAnalyzer()
