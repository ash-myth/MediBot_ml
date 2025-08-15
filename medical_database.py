"""
Comprehensive Medical Database
Contains over 1000 diseases with detailed symptom mappings for ML training
"""

import sqlite3
import json
from typing import Dict, List, Tuple, Optional
import os
from datetime import datetime

class MedicalDatabase:
    def __init__(self, db_path: str = "medical_database.db"):
        self.db_path = db_path
        self.conn = None
        self.initialize_database()
    
    def connect(self):
        """Connect to the database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def initialize_database(self):
        """Create database tables and populate with comprehensive medical data"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Create tables
        cursor.executescript("""
        -- Diseases table
        CREATE TABLE IF NOT EXISTS diseases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL,
            severity TEXT NOT NULL CHECK (severity IN ('mild', 'moderate', 'severe')),
            description TEXT,
            icd10_code TEXT,
            prevalence TEXT,
            age_group TEXT,
            gender_predisposition TEXT,
            is_emergency BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Symptoms table
        CREATE TABLE IF NOT EXISTS symptoms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL,
            severity TEXT CHECK (severity IN ('mild', 'moderate', 'severe')),
            is_emergency BOOLEAN DEFAULT 0,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Disease-Symptom relationships with probability weights
        CREATE TABLE IF NOT EXISTS disease_symptoms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease_id INTEGER NOT NULL,
            symptom_id INTEGER NOT NULL,
            probability REAL NOT NULL CHECK (probability >= 0 AND probability <= 1),
            severity_modifier REAL DEFAULT 1.0,
            is_pathognomonic BOOLEAN DEFAULT 0,
            FOREIGN KEY (disease_id) REFERENCES diseases (id),
            FOREIGN KEY (symptom_id) REFERENCES symptoms (id),
            UNIQUE(disease_id, symptom_id)
        );
        
        -- Treatment recommendations
        CREATE TABLE IF NOT EXISTS treatments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease_id INTEGER NOT NULL,
            treatment_type TEXT NOT NULL CHECK (treatment_type IN ('medication', 'lifestyle', 'procedure', 'emergency')),
            description TEXT NOT NULL,
            priority INTEGER DEFAULT 0,
            FOREIGN KEY (disease_id) REFERENCES diseases (id)
        );
        
        -- Prevention strategies
        CREATE TABLE IF NOT EXISTS prevention (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease_id INTEGER NOT NULL,
            strategy TEXT NOT NULL,
            effectiveness TEXT CHECK (effectiveness IN ('low', 'moderate', 'high')),
            FOREIGN KEY (disease_id) REFERENCES diseases (id)
        );
        
        -- Create indexes for better performance
        CREATE INDEX IF NOT EXISTS idx_disease_category ON diseases(category);
        CREATE INDEX IF NOT EXISTS idx_disease_severity ON diseases(severity);
        CREATE INDEX IF NOT EXISTS idx_symptom_category ON symptoms(category);
        CREATE INDEX IF NOT EXISTS idx_disease_symptoms_disease ON disease_symptoms(disease_id);
        CREATE INDEX IF NOT EXISTS idx_disease_symptoms_symptom ON disease_symptoms(symptom_id);
        """)
        
        conn.commit()
        
        # Check if database is already populated
        cursor.execute("SELECT COUNT(*) FROM diseases")
        disease_count = cursor.fetchone()[0]
        
        if disease_count == 0:
            print("🏥 Populating medical database with comprehensive disease data...")
            self.populate_comprehensive_database(conn)
            print(f"✅ Medical database initialized with {disease_count} diseases")
        else:
            print(f"📋 Medical database already contains {disease_count} diseases")
        
        self.close()
    
    def populate_comprehensive_database(self, conn):
        """Populate database with over 1000 diseases and their symptoms"""
        cursor = conn.cursor()
        
        # First, add all symptoms
        symptoms_data = self.get_comprehensive_symptoms()
        for symptom in symptoms_data:
            cursor.execute("""
                INSERT OR IGNORE INTO symptoms (name, category, severity, is_emergency, description)
                VALUES (?, ?, ?, ?, ?)
            """, (
                symptom['name'],
                symptom['category'],
                symptom.get('severity'),
                symptom.get('is_emergency', 0),
                symptom.get('description', '')
            ))
        
        # Then add all diseases
        diseases_data = self.get_comprehensive_diseases()
        for disease in diseases_data:
            cursor.execute("""
                INSERT OR IGNORE INTO diseases 
                (name, category, severity, description, icd10_code, prevalence, age_group, 
                 gender_predisposition, is_emergency)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                disease['name'],
                disease['category'],
                disease['severity'],
                disease.get('description', ''),
                disease.get('icd10_code', ''),
                disease.get('prevalence', ''),
                disease.get('age_group', 'all'),
                disease.get('gender_predisposition', 'both'),
                disease.get('is_emergency', 0)
            ))
            
            # Get disease ID
            cursor.execute("SELECT id FROM diseases WHERE name = ?", (disease['name'],))
            disease_id = cursor.fetchone()[0]
            
            # Add disease-symptom relationships
            for symptom_rel in disease.get('symptoms', []):
                cursor.execute("SELECT id FROM symptoms WHERE name = ?", (symptom_rel['symptom'],))
                symptom_row = cursor.fetchone()
                if symptom_row:
                    symptom_id = symptom_row[0]
                    cursor.execute("""
                        INSERT OR IGNORE INTO disease_symptoms 
                        (disease_id, symptom_id, probability, severity_modifier, is_pathognomonic)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        disease_id,
                        symptom_id,
                        symptom_rel.get('probability', 0.5),
                        symptom_rel.get('severity_modifier', 1.0),
                        symptom_rel.get('is_pathognomonic', 0)
                    ))
            
            # Add treatments
            for treatment in disease.get('treatments', []):
                cursor.execute("""
                    INSERT INTO treatments (disease_id, treatment_type, description, priority)
                    VALUES (?, ?, ?, ?)
                """, (
                    disease_id,
                    treatment.get('type', 'lifestyle'),
                    treatment['description'],
                    treatment.get('priority', 0)
                ))
            
            # Add prevention strategies
            for prevention in disease.get('prevention', []):
                cursor.execute("""
                    INSERT INTO prevention (disease_id, strategy, effectiveness)
                    VALUES (?, ?, ?)
                """, (
                    disease_id,
                    prevention['strategy'],
                    prevention.get('effectiveness', 'moderate')
                ))
        
        conn.commit()
        
        # Print statistics
        cursor.execute("SELECT COUNT(*) FROM diseases")
        disease_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM symptoms")
        symptom_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM disease_symptoms")
        relationship_count = cursor.fetchone()[0]
        
        print(f"📊 Database populated:")
        print(f"   • {disease_count} diseases")
        print(f"   • {symptom_count} symptoms") 
        print(f"   • {relationship_count} disease-symptom relationships")
    
    def get_comprehensive_symptoms(self) -> List[Dict]:
        """Return comprehensive list of medical symptoms"""
        return [
            # Constitutional Symptoms
            {"name": "fever", "category": "constitutional", "severity": "moderate", "description": "Elevated body temperature"},
            {"name": "chills", "category": "constitutional", "severity": "mild", "description": "Feeling of coldness with shivering"},
            {"name": "fatigue", "category": "constitutional", "severity": "mild", "description": "Extreme tiredness"},
            {"name": "weakness", "category": "constitutional", "severity": "mild", "description": "Lack of physical strength"},
            {"name": "malaise", "category": "constitutional", "severity": "mild", "description": "General feeling of discomfort"},
            {"name": "weight_loss", "category": "constitutional", "severity": "moderate", "description": "Unintentional weight reduction"},
            {"name": "weight_gain", "category": "constitutional", "severity": "mild", "description": "Unintentional weight increase"},
            {"name": "night_sweats", "category": "constitutional", "severity": "moderate", "description": "Excessive sweating during sleep"},
            {"name": "loss_of_appetite", "category": "constitutional", "severity": "mild", "description": "Reduced desire to eat"},
            {"name": "dehydration", "category": "constitutional", "severity": "moderate", "description": "Excessive loss of body water"},
            
            # Cardiovascular Symptoms
            {"name": "chest_pain", "category": "cardiovascular", "severity": "severe", "is_emergency": 1, "description": "Pain or discomfort in chest area"},
            {"name": "palpitations", "category": "cardiovascular", "severity": "moderate", "description": "Feeling of irregular heartbeat"},
            {"name": "shortness_of_breath", "category": "cardiovascular", "severity": "moderate", "description": "Difficulty breathing"},
            {"name": "dyspnea_on_exertion", "category": "cardiovascular", "severity": "moderate", "description": "Shortness of breath with activity"},
            {"name": "orthopnea", "category": "cardiovascular", "severity": "moderate", "description": "Difficulty breathing when lying flat"},
            {"name": "peripheral_edema", "category": "cardiovascular", "severity": "moderate", "description": "Swelling in arms or legs"},
            {"name": "cyanosis", "category": "cardiovascular", "severity": "severe", "is_emergency": 1, "description": "Bluish discoloration of skin"},
            {"name": "syncope", "category": "cardiovascular", "severity": "severe", "is_emergency": 1, "description": "Fainting or loss of consciousness"},
            {"name": "presyncope", "category": "cardiovascular", "severity": "moderate", "description": "Feeling like about to faint"},
            {"name": "claudication", "category": "cardiovascular", "severity": "moderate", "description": "Pain in legs with walking"},
            
            # Respiratory Symptoms
            {"name": "cough", "category": "respiratory", "severity": "mild", "description": "Forceful expulsion of air from lungs"},
            {"name": "productive_cough", "category": "respiratory", "severity": "moderate", "description": "Cough with sputum production"},
            {"name": "dry_cough", "category": "respiratory", "severity": "mild", "description": "Cough without sputum"},
            {"name": "hemoptysis", "category": "respiratory", "severity": "severe", "is_emergency": 1, "description": "Coughing up blood"},
            {"name": "wheeze", "category": "respiratory", "severity": "moderate", "description": "High-pitched breathing sound"},
            {"name": "stridor", "category": "respiratory", "severity": "severe", "is_emergency": 1, "description": "Loud breathing sound"},
            {"name": "sputum_production", "category": "respiratory", "severity": "moderate", "description": "Production of mucus from lungs"},
            {"name": "pleuritic_chest_pain", "category": "respiratory", "severity": "moderate", "description": "Sharp chest pain with breathing"},
            {"name": "tachypnea", "category": "respiratory", "severity": "moderate", "description": "Rapid breathing"},
            {"name": "apnea", "category": "respiratory", "severity": "severe", "is_emergency": 1, "description": "Cessation of breathing"},
            
            # Gastrointestinal Symptoms
            {"name": "nausea", "category": "gastrointestinal", "severity": "mild", "description": "Feeling of sickness with urge to vomit"},
            {"name": "vomiting", "category": "gastrointestinal", "severity": "moderate", "description": "Forceful expulsion of stomach contents"},
            {"name": "hematemesis", "category": "gastrointestinal", "severity": "severe", "is_emergency": 1, "description": "Vomiting blood"},
            {"name": "diarrhea", "category": "gastrointestinal", "severity": "mild", "description": "Loose or watery stools"},
            {"name": "constipation", "category": "gastrointestinal", "severity": "mild", "description": "Difficulty passing stools"},
            {"name": "abdominal_pain", "category": "gastrointestinal", "severity": "moderate", "description": "Pain in abdomen"},
            {"name": "bloating", "category": "gastrointestinal", "severity": "mild", "description": "Feeling of fullness in abdomen"},
            {"name": "heartburn", "category": "gastrointestinal", "severity": "mild", "description": "Burning sensation in chest"},
            {"name": "dysphagia", "category": "gastrointestinal", "severity": "moderate", "description": "Difficulty swallowing"},
            {"name": "melena", "category": "gastrointestinal", "severity": "severe", "is_emergency": 1, "description": "Black tarry stools"},
            {"name": "hematochezia", "category": "gastrointestinal", "severity": "severe", "is_emergency": 1, "description": "Blood in stool"},
            {"name": "tenesmus", "category": "gastrointestinal", "severity": "moderate", "description": "Feeling of incomplete bowel emptying"},
            
            # Neurological Symptoms
            {"name": "headache", "category": "neurological", "severity": "mild", "description": "Pain in head or upper neck"},
            {"name": "severe_headache", "category": "neurological", "severity": "severe", "is_emergency": 1, "description": "Sudden severe headache"},
            {"name": "dizziness", "category": "neurological", "severity": "mild", "description": "Feeling unsteady or lightheaded"},
            {"name": "vertigo", "category": "neurological", "severity": "moderate", "description": "Sensation of spinning"},
            {"name": "confusion", "category": "neurological", "severity": "moderate", "description": "Difficulty thinking clearly"},
            {"name": "memory_loss", "category": "neurological", "severity": "moderate", "description": "Difficulty remembering"},
            {"name": "seizure", "category": "neurological", "severity": "severe", "is_emergency": 1, "description": "Abnormal electrical activity in brain"},
            {"name": "tremor", "category": "neurological", "severity": "mild", "description": "Involuntary shaking"},
            {"name": "numbness", "category": "neurological", "severity": "moderate", "description": "Loss of sensation"},
            {"name": "tingling", "category": "neurological", "severity": "mild", "description": "Pins and needles sensation"},
            {"name": "paralysis", "category": "neurological", "severity": "severe", "is_emergency": 1, "description": "Loss of muscle function"},
            {"name": "weakness_unilateral", "category": "neurological", "severity": "severe", "is_emergency": 1, "description": "Weakness on one side"},
            {"name": "speech_difficulty", "category": "neurological", "severity": "severe", "is_emergency": 1, "description": "Problems with speech"},
            {"name": "visual_changes", "category": "neurological", "severity": "moderate", "description": "Changes in vision"},
            {"name": "tinnitus", "category": "neurological", "severity": "mild", "description": "Ringing in ears"},
            
            # Musculoskeletal Symptoms
            {"name": "muscle_pain", "category": "musculoskeletal", "severity": "mild", "description": "Pain in muscles"},
            {"name": "joint_pain", "category": "musculoskeletal", "severity": "mild", "description": "Pain in joints"},
            {"name": "joint_swelling", "category": "musculoskeletal", "severity": "moderate", "description": "Swelling of joints"},
            {"name": "stiffness", "category": "musculoskeletal", "severity": "mild", "description": "Difficulty moving joints"},
            {"name": "back_pain", "category": "musculoskeletal", "severity": "mild", "description": "Pain in back"},
            {"name": "neck_pain", "category": "musculoskeletal", "severity": "mild", "description": "Pain in neck"},
            {"name": "muscle_weakness", "category": "musculoskeletal", "severity": "moderate", "description": "Reduced muscle strength"},
            {"name": "muscle_cramps", "category": "musculoskeletal", "severity": "mild", "description": "Painful muscle contractions"},
            {"name": "bone_pain", "category": "musculoskeletal", "severity": "moderate", "description": "Deep aching pain in bones"},
            
            
            # Dermatological Symptoms
            {"name": "rash", "category": "dermatological", "severity": "mild", "description": "Skin irritation or eruption"},
            {"name": "itching", "category": "dermatological", "severity": "mild", "description": "Desire to scratch skin"},
            {"name": "skin_lesions", "category": "dermatological", "severity": "moderate", "description": "Abnormal skin growths"},
            {"name": "bruising", "category": "dermatological", "severity": "mild", "description": "Discoloration from bleeding"},
            {"name": "pallor", "category": "dermatological", "severity": "moderate", "description": "Pale skin color"},
            {"name": "jaundice", "category": "dermatological", "severity": "moderate", "description": "Yellow discoloration of skin"},
            {"name": "petechiae", "category": "dermatological", "severity": "moderate", "description": "Small red or purple spots"},
            {"name": "ulcers", "category": "dermatological", "severity": "moderate", "description": "Open sores on skin"},
            {"name": "nodules", "category": "dermatological", "severity": "moderate", "description": "Firm bumps under skin"},
            
            # Genitourinary Symptoms
            {"name": "dysuria", "category": "genitourinary", "severity": "mild", "description": "Painful urination"},
            {"name": "frequency", "category": "genitourinary", "severity": "mild", "description": "Frequent urination"},
            {"name": "urgency", "category": "genitourinary", "severity": "mild", "description": "Sudden need to urinate"},
            {"name": "hematuria", "category": "genitourinary", "severity": "moderate", "description": "Blood in urine"},
            {"name": "oliguria", "category": "genitourinary", "severity": "moderate", "description": "Decreased urine output"},
            {"name": "anuria", "category": "genitourinary", "severity": "severe", "is_emergency": 1, "description": "Absence of urine production"},
            {"name": "nocturia", "category": "genitourinary", "severity": "mild", "description": "Frequent urination at night"},
            {"name": "incontinence", "category": "genitourinary", "severity": "moderate", "description": "Loss of bladder control"},
            
            # Ophthalmological Symptoms
            {"name": "eye_pain", "category": "ophthalmological", "severity": "moderate", "description": "Pain in or around eye"},
            {"name": "blurred_vision", "category": "ophthalmological", "severity": "moderate", "description": "Unclear or fuzzy vision"},
            {"name": "double_vision", "category": "ophthalmological", "severity": "moderate", "description": "Seeing two images"},
            {"name": "photophobia", "category": "ophthalmological", "severity": "moderate", "description": "Sensitivity to light"},
            {"name": "eye_discharge", "category": "ophthalmological", "severity": "mild", "description": "Fluid from eye"},
            {"name": "red_eye", "category": "ophthalmological", "severity": "mild", "description": "Bloodshot or red eye"},
            {"name": "sudden_vision_loss", "category": "ophthalmological", "severity": "severe", "is_emergency": 1, "description": "Sudden loss of sight"},
            
            # ENT Symptoms
            {"name": "sore_throat", "category": "ent", "severity": "mild", "description": "Pain or scratchiness in throat"},
            {"name": "runny_nose", "category": "ent", "severity": "mild", "description": "Nasal discharge"},
            {"name": "nasal_congestion", "category": "ent", "severity": "mild", "description": "Blocked nose"},
            {"name": "sneezing", "category": "ent", "severity": "mild", "description": "Forceful expulsion of air through nose"},
            {"name": "ear_pain", "category": "ent", "severity": "mild", "description": "Pain in ear"},
            {"name": "hearing_loss", "category": "ent", "severity": "moderate", "description": "Reduced ability to hear"},
            {"name": "ear_discharge", "category": "ent", "severity": "moderate", "description": "Fluid from ear"},
            {"name": "hoarseness", "category": "ent", "severity": "mild", "description": "Rough or harsh voice"},
            {"name": "loss_of_smell", "category": "ent", "severity": "mild", "description": "Inability to smell"},
            {"name": "loss_of_taste", "category": "ent", "severity": "mild", "description": "Inability to taste"},
            
            # Psychiatric Symptoms
            {"name": "anxiety", "category": "psychiatric", "severity": "moderate", "description": "Feeling of worry or unease"},
            {"name": "depression", "category": "psychiatric", "severity": "moderate", "description": "Persistent sadness"},
            {"name": "irritability", "category": "psychiatric", "severity": "mild", "description": "Easily annoyed or angered"},
            {"name": "mood_changes", "category": "psychiatric", "severity": "moderate", "description": "Fluctuations in emotional state"},
            {"name": "sleep_disturbance", "category": "psychiatric", "severity": "mild", "description": "Difficulty with sleep"},
            {"name": "concentration_difficulty", "category": "psychiatric", "severity": "mild", "description": "Trouble focusing"},
            {"name": "panic_attacks", "category": "psychiatric", "severity": "severe", "description": "Episodes of intense fear"},
            {"name": "hallucinations", "category": "psychiatric", "severity": "severe", "description": "Seeing or hearing things that aren't there"},
            {"name": "delusions", "category": "psychiatric", "severity": "severe", "description": "False beliefs"},
            
            # Endocrine Symptoms
            {"name": "polyuria", "category": "endocrine", "severity": "moderate", "description": "Excessive urination"},
            {"name": "polydipsia", "category": "endocrine", "severity": "moderate", "description": "Excessive thirst"},
            {"name": "polyphagia", "category": "endocrine", "severity": "moderate", "description": "Excessive hunger"},
            {"name": "heat_intolerance", "category": "endocrine", "severity": "mild", "description": "Sensitivity to heat"},
            {"name": "cold_intolerance", "category": "endocrine", "severity": "mild", "description": "Sensitivity to cold"},
            {"name": "hair_loss", "category": "endocrine", "severity": "mild", "description": "Loss of hair"},
            {"name": "excessive_hair_growth", "category": "endocrine", "severity": "mild", "description": "Abnormal hair growth"},
            
            # Hematological Symptoms
            {"name": "easy_bruising", "category": "hematological", "severity": "moderate", "description": "Bruising with minimal trauma"},
            {"name": "bleeding_gums", "category": "hematological", "severity": "moderate", "description": "Bleeding from gums"},
            {"name": "nosebleeds", "category": "hematological", "severity": "mild", "description": "Bleeding from nose"},
            {"name": "lymphadenopathy", "category": "hematological", "severity": "moderate", "description": "Swollen lymph nodes"},
            {"name": "splenomegaly", "category": "hematological", "severity": "moderate", "description": "Enlarged spleen"},
            
            # Additional Common Symptoms
            {"name": "swelling", "category": "general", "severity": "mild", "description": "Enlargement due to fluid accumulation"},
            {"name": "inflammation", "category": "general", "severity": "mild", "description": "Redness, heat, swelling, pain"},
            {"name": "discharge", "category": "general", "severity": "mild", "description": "Abnormal secretion"},
            {"name": "odor", "category": "general", "severity": "mild", "description": "Unusual smell"},
            {"name": "tenderness", "category": "general", "severity": "mild", "description": "Pain when touched"},
            {"name": "burning_sensation", "category": "general", "severity": "mild", "description": "Feeling of burning"},
            {"name": "cramping", "category": "general", "severity": "mild", "description": "Painful muscle contractions"}
        ]
    
    def get_comprehensive_diseases(self) -> List[Dict]:
        """Return comprehensive list of over 1000 diseases with symptoms"""
        # Import the comprehensive disease dataset
        try:
            from disease_data_1000 import get_1000_plus_diseases
            diseases = get_1000_plus_diseases()
            print(f"✅ Loaded {len(diseases)} comprehensive diseases from dataset")
            return diseases
        except ImportError:
            print("⚠️ Could not import comprehensive disease dataset, using basic set")
            # Fallback to basic diseases if import fails
            return self._get_basic_diseases()
    
    def _get_basic_diseases(self) -> List[Dict]:
        """Fallback basic disease set if comprehensive dataset unavailable"""
        return [
            {
                "name": "Influenza A",
                "category": "infectious",
                "severity": "moderate",
                "icd10_code": "J09",
                "description": "Viral respiratory infection caused by influenza A virus",
                "symptoms": [
                    {"symptom": "fever", "probability": 0.9},
                    {"symptom": "chills", "probability": 0.8},
                    {"symptom": "muscle_pain", "probability": 0.9},
                    {"symptom": "headache", "probability": 0.8},
                    {"symptom": "fatigue", "probability": 0.9},
                    {"symptom": "cough", "probability": 0.7},
                    {"symptom": "sore_throat", "probability": 0.6}
                ]
            },
            {
                "name": "Common Cold",
                "category": "infectious",
                "severity": "mild",
                "icd10_code": "J00",
                "description": "Viral upper respiratory tract infection",
                "symptoms": [
                    {"symptom": "runny_nose", "probability": 0.9},
                    {"symptom": "nasal_congestion", "probability": 0.85},
                    {"symptom": "sneezing", "probability": 0.8},
                    {"symptom": "sore_throat", "probability": 0.7},
                    {"symptom": "cough", "probability": 0.6},
                    {"symptom": "headache", "probability": 0.4},
                    {"symptom": "fatigue", "probability": 0.5}
                ]
            }
        ]
    
    def get_training_data_for_ml(self, limit: int = None) -> List[Dict]:
        """Get training data formatted for ML model"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Query to get disease-symptom relationships with descriptions
        query = """
        SELECT 
            d.name as disease,
            d.category,
            d.severity,
            GROUP_CONCAT(s.name) as symptoms,
            d.description
        FROM diseases d
        JOIN disease_symptoms ds ON d.id = ds.disease_id
        JOIN symptoms s ON ds.symptom_id = s.id
        WHERE ds.probability > 0.3
        GROUP BY d.id, d.name, d.category, d.severity, d.description
        """
        
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        training_data = []
        for row in results:
            symptoms_list = row['symptoms'].split(',')
            
            # Create symptom description
            description = ' '.join(symptoms_list)
            if row['description']:
                description += ' ' + row['description']
            
            training_data.append({
                'description': description,
                'symptoms': symptoms_list,
                'disease': row['disease'].lower().replace(' ', '_').replace('-', '_'),
                'severity': row['severity']
            })
        
        self.close()
        return training_data
    
    def search_diseases_by_symptoms(self, symptoms: List[str], threshold: float = 0.3) -> List[Dict]:
        """Search for diseases based on symptoms"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Create placeholders for symptoms
        symptom_placeholders = ','.join(['?'] * len(symptoms))
        
        query = """
        SELECT 
            d.name,
            d.category,
            d.severity,
            d.description,
            COUNT(ds.symptom_id) as matching_symptoms,
            AVG(ds.probability) as avg_probability
        FROM diseases d
        JOIN disease_symptoms ds ON d.id = ds.disease_id
        JOIN symptoms s ON ds.symptom_id = s.id
        WHERE s.name IN ({})
        GROUP BY d.id
        HAVING avg_probability >= ?
        ORDER BY matching_symptoms DESC, avg_probability DESC
        LIMIT 10
        """.format(symptom_placeholders)
        
        cursor.execute(query, symptoms + [threshold])
        results = cursor.fetchall()
        
        diseases = []
        for row in results:
            diseases.append({
                'name': row['name'],
                'category': row['category'],
                'severity': row['severity'],
                'description': row['description'],
                'matching_symptoms': row['matching_symptoms'],
                'probability': row['avg_probability']
            })
        
        self.close()
        return diseases
    
    def get_disease_info(self, disease_name: str) -> Dict:
        """Get comprehensive information about a disease"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Get disease basic info
        cursor.execute("""
            SELECT * FROM diseases WHERE name = ? OR name LIKE ?
        """, (disease_name, f"%{disease_name}%"))
        
        disease = cursor.fetchone()
        if not disease:
            self.close()
            return {"error": "Disease not found"}
        
        disease_dict = dict(disease)
        
        # Get symptoms
        cursor.execute("""
            SELECT s.name, s.category, ds.probability, ds.is_pathognomonic
            FROM symptoms s
            JOIN disease_symptoms ds ON s.id = ds.symptom_id
            WHERE ds.disease_id = ?
            ORDER BY ds.probability DESC
        """, (disease['id'],))
        
        symptoms = cursor.fetchall()
        disease_dict['symptoms'] = [dict(row) for row in symptoms]
        
        # Get treatments
        cursor.execute("""
            SELECT treatment_type, description, priority
            FROM treatments
            WHERE disease_id = ?
            ORDER BY priority DESC
        """, (disease['id'],))
        
        treatments = cursor.fetchall()
        disease_dict['treatments'] = [dict(row) for row in treatments]
        
        # Get prevention strategies
        cursor.execute("""
            SELECT strategy, effectiveness
            FROM prevention
            WHERE disease_id = ?
        """, (disease['id'],))
        
        prevention = cursor.fetchall()
        disease_dict['prevention'] = [dict(row) for row in prevention]
        
        self.close()
        return disease_dict

# Create global database instance
medical_db = MedicalDatabase()
