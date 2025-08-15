"""
Database Management Utilities
Tools for managing, updating, and maintaining the comprehensive medical database
"""

import sqlite3
import json
import csv
from typing import Dict, List, Optional, Any
from datetime import datetime
import os
from medical_database import medical_db

class DatabaseManager:
    def __init__(self, db_path: str = "medical_database.db"):
        self.db_path = db_path
    
    def get_database_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Count diseases by category
        cursor.execute("""
            SELECT category, COUNT(*) as count 
            FROM diseases 
            GROUP BY category 
            ORDER BY count DESC
        """)
        stats['diseases_by_category'] = dict(cursor.fetchall())
        
        # Count symptoms by category
        cursor.execute("""
            SELECT category, COUNT(*) as count 
            FROM symptoms 
            GROUP BY category 
            ORDER BY count DESC
        """)
        stats['symptoms_by_category'] = dict(cursor.fetchall())
        
        # Count diseases by severity
        cursor.execute("""
            SELECT severity, COUNT(*) as count 
            FROM diseases 
            GROUP BY severity 
            ORDER BY count DESC
        """)
        stats['diseases_by_severity'] = dict(cursor.fetchall())
        
        # Emergency diseases count
        cursor.execute("SELECT COUNT(*) FROM diseases WHERE is_emergency = 1")
        stats['emergency_diseases'] = cursor.fetchone()[0]
        
        # Total counts
        cursor.execute("SELECT COUNT(*) FROM diseases")
        stats['total_diseases'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM symptoms")
        stats['total_symptoms'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM disease_symptoms")
        stats['total_relationships'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM treatments")
        stats['total_treatments'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM prevention")
        stats['total_preventions'] = cursor.fetchone()[0]
        
        # Top diseases with most symptoms
        cursor.execute("""
            SELECT d.name, COUNT(ds.symptom_id) as symptom_count
            FROM diseases d
            JOIN disease_symptoms ds ON d.id = ds.disease_id
            GROUP BY d.id, d.name
            ORDER BY symptom_count DESC
            LIMIT 10
        """)
        stats['diseases_most_symptoms'] = dict(cursor.fetchall())
        
        conn.close()
        return stats
    
    def search_diseases(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for diseases by name or description"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, category, severity, description, icd10_code
            FROM diseases
            WHERE name LIKE ? OR description LIKE ?
            ORDER BY 
                CASE 
                    WHEN name LIKE ? THEN 1
                    WHEN description LIKE ? THEN 2
                    ELSE 3
                END,
                name
            LIMIT ?
        """, (f"%{query}%", f"%{query}%", f"{query}%", f"{query}%", limit))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def search_symptoms(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for symptoms by name or description"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, category, severity, description, is_emergency
            FROM symptoms
            WHERE name LIKE ? OR description LIKE ?
            ORDER BY 
                CASE 
                    WHEN name LIKE ? THEN 1
                    WHEN description LIKE ? THEN 2
                    ELSE 3
                END,
                name
            LIMIT ?
        """, (f"%{query}%", f"%{query}%", f"{query}%", f"{query}%", limit))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def get_disease_details(self, disease_id: int) -> Dict:
        """Get comprehensive details about a specific disease"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get disease basic info
        cursor.execute("SELECT * FROM diseases WHERE id = ?", (disease_id,))
        disease = cursor.fetchone()
        
        if not disease:
            conn.close()
            return {"error": "Disease not found"}
        
        disease_dict = dict(disease)
        
        # Get symptoms with probabilities
        cursor.execute("""
            SELECT s.name, s.category, s.description, ds.probability, ds.is_pathognomonic
            FROM symptoms s
            JOIN disease_symptoms ds ON s.id = ds.symptom_id
            WHERE ds.disease_id = ?
            ORDER BY ds.probability DESC
        """, (disease_id,))
        disease_dict['symptoms'] = [dict(row) for row in cursor.fetchall()]
        
        # Get treatments
        cursor.execute("""
            SELECT treatment_type, description, priority
            FROM treatments
            WHERE disease_id = ?
            ORDER BY priority DESC, treatment_type
        """, (disease_id,))
        disease_dict['treatments'] = [dict(row) for row in cursor.fetchall()]
        
        # Get prevention strategies
        cursor.execute("""
            SELECT strategy, effectiveness
            FROM prevention
            WHERE disease_id = ?
            ORDER BY effectiveness DESC
        """, (disease_id,))
        disease_dict['prevention'] = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return disease_dict
    
    def add_disease(self, disease_data: Dict) -> int:
        """Add a new disease to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insert disease
        cursor.execute("""
            INSERT INTO diseases 
            (name, category, severity, description, icd10_code, prevalence, 
             age_group, gender_predisposition, is_emergency)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            disease_data['name'],
            disease_data['category'],
            disease_data['severity'],
            disease_data.get('description', ''),
            disease_data.get('icd10_code', ''),
            disease_data.get('prevalence', ''),
            disease_data.get('age_group', 'all'),
            disease_data.get('gender_predisposition', 'both'),
            disease_data.get('is_emergency', 0)
        ))
        
        disease_id = cursor.lastrowid
        
        # Add symptoms if provided
        if 'symptoms' in disease_data:
            for symptom in disease_data['symptoms']:
                # Find or create symptom
                cursor.execute("SELECT id FROM symptoms WHERE name = ?", (symptom['symptom'],))
                symptom_row = cursor.fetchone()
                
                if symptom_row:
                    symptom_id = symptom_row[0]
                else:
                    # Create new symptom
                    cursor.execute("""
                        INSERT INTO symptoms (name, category, description)
                        VALUES (?, ?, ?)
                    """, (symptom['symptom'], 'general', ''))
                    symptom_id = cursor.lastrowid
                
                # Link disease and symptom
                cursor.execute("""
                    INSERT INTO disease_symptoms 
                    (disease_id, symptom_id, probability, is_pathognomonic)
                    VALUES (?, ?, ?, ?)
                """, (
                    disease_id,
                    symptom_id,
                    symptom.get('probability', 0.5),
                    symptom.get('is_pathognomonic', 0)
                ))
        
        # Add treatments if provided
        if 'treatments' in disease_data:
            for treatment in disease_data['treatments']:
                cursor.execute("""
                    INSERT INTO treatments (disease_id, treatment_type, description, priority)
                    VALUES (?, ?, ?, ?)
                """, (
                    disease_id,
                    treatment.get('type', 'lifestyle'),
                    treatment['description'],
                    treatment.get('priority', 0)
                ))
        
        # Add prevention strategies if provided
        if 'prevention' in disease_data:
            for prevention in disease_data['prevention']:
                cursor.execute("""
                    INSERT INTO prevention (disease_id, strategy, effectiveness)
                    VALUES (?, ?, ?)
                """, (
                    disease_id,
                    prevention['strategy'],
                    prevention.get('effectiveness', 'moderate')
                ))
        
        conn.commit()
        conn.close()
        return disease_id
    
    def update_disease(self, disease_id: int, updates: Dict) -> bool:
        """Update an existing disease"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build update query dynamically
        valid_fields = ['name', 'category', 'severity', 'description', 'icd10_code', 
                       'prevalence', 'age_group', 'gender_predisposition', 'is_emergency']
        
        update_fields = []
        update_values = []
        
        for field, value in updates.items():
            if field in valid_fields:
                update_fields.append(f"{field} = ?")
                update_values.append(value)
        
        if not update_fields:
            conn.close()
            return False
        
        update_values.append(disease_id)
        
        query = f"UPDATE diseases SET {', '.join(update_fields)} WHERE id = ?"
        cursor.execute(query, update_values)
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    def delete_disease(self, disease_id: int) -> bool:
        """Delete a disease and all its relationships"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Delete related data first
            cursor.execute("DELETE FROM disease_symptoms WHERE disease_id = ?", (disease_id,))
            cursor.execute("DELETE FROM treatments WHERE disease_id = ?", (disease_id,))
            cursor.execute("DELETE FROM prevention WHERE disease_id = ?", (disease_id,))
            
            # Delete the disease
            cursor.execute("DELETE FROM diseases WHERE id = ?", (disease_id,))
            
            success = cursor.rowcount > 0
            conn.commit()
        except Exception as e:
            conn.rollback()
            success = False
            print(f"Error deleting disease: {e}")
        finally:
            conn.close()
        
        return success
    
    def export_database_to_json(self, output_file: str) -> bool:
        """Export the entire database to a JSON file"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            export_data = {
                'export_timestamp': datetime.now().isoformat(),
                'diseases': [],
                'symptoms': []
            }
            
            # Export diseases with all relationships
            cursor.execute("SELECT * FROM diseases ORDER BY category, name")
            for disease_row in cursor.fetchall():
                disease = dict(disease_row)
                disease_id = disease['id']
                
                # Get symptoms
                cursor.execute("""
                    SELECT s.name, s.category, s.description, ds.probability, ds.is_pathognomonic
                    FROM symptoms s
                    JOIN disease_symptoms ds ON s.id = ds.symptom_id
                    WHERE ds.disease_id = ?
                    ORDER BY ds.probability DESC
                """, (disease_id,))
                disease['symptoms'] = [dict(row) for row in cursor.fetchall()]
                
                # Get treatments
                cursor.execute("""
                    SELECT treatment_type, description, priority
                    FROM treatments
                    WHERE disease_id = ?
                    ORDER BY priority DESC
                """, (disease_id,))
                disease['treatments'] = [dict(row) for row in cursor.fetchall()]
                
                # Get prevention
                cursor.execute("""
                    SELECT strategy, effectiveness
                    FROM prevention
                    WHERE disease_id = ?
                """, (disease_id,))
                disease['prevention'] = [dict(row) for row in cursor.fetchall()]
                
                export_data['diseases'].append(disease)
            
            # Export symptoms
            cursor.execute("SELECT * FROM symptoms ORDER BY category, name")
            export_data['symptoms'] = [dict(row) for row in cursor.fetchall()]
            
            # Write to file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error exporting database: {e}")
            return False
    
    def import_database_from_json(self, input_file: str, merge: bool = False) -> bool:
        """Import database from a JSON file"""
        try:
            if not os.path.exists(input_file):
                print(f"Import file not found: {input_file}")
                return False
            
            with open(input_file, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if not merge:
                # Clear existing data
                cursor.execute("DELETE FROM prevention")
                cursor.execute("DELETE FROM treatments") 
                cursor.execute("DELETE FROM disease_symptoms")
                cursor.execute("DELETE FROM diseases")
                cursor.execute("DELETE FROM symptoms")
            
            # Import symptoms first
            for symptom in import_data.get('symptoms', []):
                cursor.execute("""
                    INSERT OR IGNORE INTO symptoms 
                    (name, category, severity, is_emergency, description)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    symptom['name'],
                    symptom['category'],
                    symptom.get('severity'),
                    symptom.get('is_emergency', 0),
                    symptom.get('description', '')
                ))
            
            # Import diseases
            for disease in import_data.get('diseases', []):
                # Insert disease
                cursor.execute("""
                    INSERT OR IGNORE INTO diseases 
                    (name, category, severity, description, icd10_code, prevalence, 
                     age_group, gender_predisposition, is_emergency)
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
                
                # Import symptoms relationships
                for symptom_rel in disease.get('symptoms', []):
                    cursor.execute("SELECT id FROM symptoms WHERE name = ?", (symptom_rel['name'],))
                    symptom_row = cursor.fetchone()
                    if symptom_row:
                        symptom_id = symptom_row[0]
                        cursor.execute("""
                            INSERT OR IGNORE INTO disease_symptoms 
                            (disease_id, symptom_id, probability, is_pathognomonic)
                            VALUES (?, ?, ?, ?)
                        """, (
                            disease_id,
                            symptom_id,
                            symptom_rel.get('probability', 0.5),
                            symptom_rel.get('is_pathognomonic', 0)
                        ))
                
                # Import treatments
                for treatment in disease.get('treatments', []):
                    cursor.execute("""
                        INSERT INTO treatments (disease_id, treatment_type, description, priority)
                        VALUES (?, ?, ?, ?)
                    """, (
                        disease_id,
                        treatment.get('treatment_type', 'lifestyle'),
                        treatment['description'],
                        treatment.get('priority', 0)
                    ))
                
                # Import prevention
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
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error importing database: {e}")
            return False
    
    def optimize_database(self) -> bool:
        """Optimize database performance"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Update statistics
            cursor.execute("ANALYZE")
            
            # Vacuum to reclaim space
            cursor.execute("VACUUM")
            
            conn.close()
            print("Database optimization completed")
            return True
            
        except Exception as e:
            print(f"Error optimizing database: {e}")
            return False
    
    def validate_database_integrity(self) -> Dict[str, List[str]]:
        """Validate database integrity and return issues found"""
        issues = {
            'missing_relationships': [],
            'invalid_probabilities': [],
            'orphaned_records': [],
            'duplicate_entries': []
        }
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check for diseases without symptoms
        cursor.execute("""
            SELECT d.name 
            FROM diseases d 
            LEFT JOIN disease_symptoms ds ON d.id = ds.disease_id 
            WHERE ds.disease_id IS NULL
        """)
        issues['missing_relationships'] = [row[0] for row in cursor.fetchall()]
        
        # Check for invalid probabilities
        cursor.execute("""
            SELECT d.name, ds.probability
            FROM diseases d
            JOIN disease_symptoms ds ON d.id = ds.disease_id
            WHERE ds.probability < 0 OR ds.probability > 1
        """)
        issues['invalid_probabilities'] = [f"{row[0]} (prob: {row[1]})" for row in cursor.fetchall()]
        
        # Check for orphaned treatments
        cursor.execute("""
            SELECT t.id, t.description
            FROM treatments t
            LEFT JOIN diseases d ON t.disease_id = d.id
            WHERE d.id IS NULL
        """)
        issues['orphaned_records'].extend([f"Treatment {row[0]}: {row[1][:50]}..." for row in cursor.fetchall()])
        
        # Check for duplicate disease names
        cursor.execute("""
            SELECT name, COUNT(*) as count
            FROM diseases
            GROUP BY name
            HAVING count > 1
        """)
        issues['duplicate_entries'] = [f"Disease: {row[0]} ({row[1]} copies)" for row in cursor.fetchall()]
        
        conn.close()
        return issues

def main():
    """Command-line interface for database management"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Medical Database Management Utilities")
    parser.add_argument('command', choices=['stats', 'search', 'export', 'import', 'validate', 'optimize'],
                       help='Command to execute')
    parser.add_argument('--query', '-q', help='Search query')
    parser.add_argument('--file', '-f', help='File path for import/export')
    parser.add_argument('--merge', action='store_true', help='Merge when importing (default: replace)')
    
    args = parser.parse_args()
    
    db_manager = DatabaseManager()
    
    if args.command == 'stats':
        stats = db_manager.get_database_statistics()
        print("📊 Database Statistics:")
        print(f"  Total diseases: {stats['total_diseases']}")
        print(f"  Total symptoms: {stats['total_symptoms']}")
        print(f"  Total relationships: {stats['total_relationships']}")
        print(f"  Emergency diseases: {stats['emergency_diseases']}")
        print("\n📈 Diseases by category:")
        for category, count in stats['diseases_by_category'].items():
            print(f"  {category}: {count}")
        
    elif args.command == 'search':
        if not args.query:
            print("Please provide a search query with --query")
            return
        
        diseases = db_manager.search_diseases(args.query)
        print(f"🔍 Found {len(diseases)} diseases matching '{args.query}':")
        for disease in diseases:
            print(f"  - {disease['name']} ({disease['category']}, {disease['severity']})")
    
    elif args.command == 'export':
        if not args.file:
            print("Please provide output file with --file")
            return
        
        success = db_manager.export_database_to_json(args.file)
        if success:
            print(f"✅ Database exported to {args.file}")
        else:
            print("❌ Export failed")
    
    elif args.command == 'import':
        if not args.file:
            print("Please provide input file with --file")
            return
        
        success = db_manager.import_database_from_json(args.file, args.merge)
        if success:
            print(f"✅ Database imported from {args.file}")
        else:
            print("❌ Import failed")
    
    elif args.command == 'validate':
        issues = db_manager.validate_database_integrity()
        print("🔍 Database Integrity Check:")
        
        total_issues = sum(len(issue_list) for issue_list in issues.values())
        if total_issues == 0:
            print("✅ No issues found!")
        else:
            print(f"❌ Found {total_issues} issues:")
            for issue_type, issue_list in issues.items():
                if issue_list:
                    print(f"\n{issue_type.replace('_', ' ').title()}:")
                    for issue in issue_list:
                        print(f"  - {issue}")
    
    elif args.command == 'optimize':
        success = db_manager.optimize_database()
        if success:
            print("✅ Database optimized successfully")
        else:
            print("❌ Optimization failed")

if __name__ == "__main__":
    main()
