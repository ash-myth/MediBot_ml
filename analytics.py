"""
Advanced Analytics and Visualization Module
Provides detailed analysis and visual representations of symptom data
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple
from collections import Counter, defaultdict

class SymptomAnalytics:
    def __init__(self):
        self.session_history = []
        self.symptom_trends = defaultdict(list)
        self.condition_accuracy = {}
        
        # Set style for visualizations
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
    
    def log_session(self, session_data: Dict):
        """Log a complete assessment session"""
        session_data['timestamp'] = datetime.now().isoformat()
        self.session_history.append(session_data)
        
        # Update trends
        for symptom, severity in session_data.get('symptoms', {}).items():
            self.symptom_trends[symptom].append({
                'timestamp': session_data['timestamp'],
                'severity': severity,
                'session_id': len(self.session_history)
            })
    
    def generate_symptom_frequency_chart(self) -> str:
        """Generate symptom frequency bar chart"""
        if not self.session_history:
            return None
        
        # Count symptom frequencies
        symptom_counts = Counter()
        for session in self.session_history:
            for symptom in session.get('symptoms', {}):
                symptom_counts[symptom.replace('_', ' ').title()] += 1
        
        # Create chart
        fig, ax = plt.subplots(figsize=(12, 8))
        symptoms = list(symptom_counts.keys())[:10]  # Top 10
        counts = [symptom_counts[s] for s in symptoms]
        
        bars = ax.bar(symptoms, counts, color=plt.cm.viridis(np.linspace(0, 1, len(symptoms))))
        ax.set_title('Most Common Symptoms', fontsize=16, fontweight='bold')
        ax.set_xlabel('Symptoms', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{count}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        # Save chart
        chart_path = "symptom_frequency_chart.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return chart_path
    
    def generate_severity_distribution(self) -> str:
        """Generate severity level distribution pie chart"""
        if not self.session_history:
            return None
        
        severity_counts = Counter()
        for session in self.session_history:
            for symptom, severity in session.get('symptoms', {}).items():
                severity_counts[severity.title()] += 1
        
        # Create pie chart
        fig, ax = plt.subplots(figsize=(10, 8))
        labels = list(severity_counts.keys())
        sizes = list(severity_counts.values())
        colors = {'Mild': '#90EE90', 'Moderate': '#FFB347', 'Severe': '#FF6B6B'}
        chart_colors = [colors.get(label, '#CCCCCC') for label in labels]
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=chart_colors, 
                                         autopct='%1.1f%%', startangle=90,
                                         textprops={'fontsize': 12, 'fontweight': 'bold'})
        
        ax.set_title('Symptom Severity Distribution', fontsize=16, fontweight='bold')
        
        # Enhance text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.tight_layout()
        
        # Save chart
        chart_path = "severity_distribution_chart.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return chart_path
    
    def generate_condition_probability_chart(self, assessment_data: Dict) -> str:
        """Generate condition probability horizontal bar chart"""
        if not assessment_data or 'conditions' not in assessment_data:
            return None
        
        conditions = assessment_data['conditions']
        
        # Create horizontal bar chart
        fig, ax = plt.subplots(figsize=(12, 8))
        condition_names = []
        probabilities = []
        
        for condition, prob in list(conditions.items())[:8]:  # Top 8
            # Convert condition name to readable format
            readable_name = condition.replace('_', ' ').title()
            condition_names.append(readable_name)
            probabilities.append(prob)
        
        # Create gradient colors based on probability
        colors = plt.cm.RdYlBu_r(np.linspace(0.2, 0.8, len(probabilities)))
        
        bars = ax.barh(condition_names, probabilities, color=colors)
        ax.set_title('Condition Probability Assessment', fontsize=16, fontweight='bold')
        ax.set_xlabel('Probability (%)', fontsize=12)
        ax.set_ylabel('Medical Conditions', fontsize=12)
        
        # Add percentage labels
        for bar, prob in zip(bars, probabilities):
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height()/2,
                   f'{prob:.1f}%', ha='left', va='center', fontweight='bold')
        
        # Set x-axis limit
        ax.set_xlim(0, max(probabilities) * 1.2)
        
        plt.tight_layout()
        
        # Save chart
        chart_path = "condition_probability_chart.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return chart_path
    
    def generate_timeline_chart(self) -> str:
        """Generate timeline of symptoms over sessions"""
        if len(self.session_history) < 2:
            return None
        
        # Prepare data
        timeline_data = []
        for i, session in enumerate(self.session_history):
            timestamp = datetime.fromisoformat(session['timestamp'])
            symptom_count = len(session.get('symptoms', {}))
            severity_score = self._calculate_session_severity(session)
            
            timeline_data.append({
                'session': i + 1,
                'timestamp': timestamp,
                'symptom_count': symptom_count,
                'severity_score': severity_score
            })
        
        df = pd.DataFrame(timeline_data)
        
        # Create timeline chart
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
        
        # Symptom count over time
        ax1.plot(df['timestamp'], df['symptom_count'], marker='o', linewidth=2, 
                markersize=8, color='#2E86AB', label='Symptom Count')
        ax1.fill_between(df['timestamp'], df['symptom_count'], alpha=0.3, color='#2E86AB')
        ax1.set_title('Symptom Timeline Analysis', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Number of Symptoms', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Severity score over time
        ax2.plot(df['timestamp'], df['severity_score'], marker='s', linewidth=2, 
                markersize=8, color='#F18F01', label='Severity Score')
        ax2.fill_between(df['timestamp'], df['severity_score'], alpha=0.3, color='#F18F01')
        ax2.set_ylabel('Severity Score', fontsize=12)
        ax2.set_xlabel('Time', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Format x-axis
        if len(df) > 1:
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
            ax2.xaxis.set_major_locator(mdates.HourLocator(interval=1))
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        # Save chart
        chart_path = "timeline_chart.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return chart_path
    
    def _calculate_session_severity(self, session: Dict) -> float:
        """Calculate overall severity score for a session"""
        symptoms = session.get('symptoms', {})
        if not symptoms:
            return 0
        
        severity_weights = {'mild': 1, 'moderate': 2, 'severe': 3}
        total_score = sum(severity_weights.get(severity, 1) for severity in symptoms.values())
        max_possible = len(symptoms) * 3
        
        return (total_score / max_possible) * 100 if max_possible > 0 else 0
    
    def generate_comprehensive_report(self, current_assessment: Dict) -> Dict[str, str]:
        """Generate comprehensive analysis report with all charts"""
        charts = {}
        
        try:
            # Generate frequency chart
            freq_chart = self.generate_symptom_frequency_chart()
            if freq_chart:
                charts['frequency'] = freq_chart
            
            # Generate severity distribution
            sev_chart = self.generate_severity_distribution()
            if sev_chart:
                charts['severity'] = sev_chart
            
            # Generate condition probability chart
            cond_chart = self.generate_condition_probability_chart(current_assessment)
            if cond_chart:
                charts['conditions'] = cond_chart
            
            # Generate timeline chart
            time_chart = self.generate_timeline_chart()
            if time_chart:
                charts['timeline'] = time_chart
            
        except Exception as e:
            print(f"Error generating charts: {e}")
        
        return charts
    
    def get_session_statistics(self) -> Dict:
        """Get comprehensive session statistics"""
        if not self.session_history:
            return {}
        
        total_sessions = len(self.session_history)
        total_symptoms = sum(len(s.get('symptoms', {})) for s in self.session_history)
        avg_symptoms_per_session = total_symptoms / total_sessions if total_sessions > 0 else 0
        
        # Most common symptoms
        symptom_counter = Counter()
        severity_counter = Counter()
        
        for session in self.session_history:
            for symptom, severity in session.get('symptoms', {}).items():
                symptom_counter[symptom] += 1
                severity_counter[severity] += 1
        
        most_common_symptoms = symptom_counter.most_common(5)
        severity_distribution = dict(severity_counter)
        
        # Calculate average severity
        severity_weights = {'mild': 1, 'moderate': 2, 'severe': 3}
        total_severity = sum(severity_weights.get(sev, 1) * count 
                           for sev, count in severity_counter.items())
        avg_severity = total_severity / sum(severity_counter.values()) if severity_counter else 0
        
        return {
            'total_sessions': total_sessions,
            'total_symptoms_recorded': total_symptoms,
            'average_symptoms_per_session': round(avg_symptoms_per_session, 2),
            'most_common_symptoms': most_common_symptoms,
            'severity_distribution': severity_distribution,
            'average_severity_score': round(avg_severity, 2),
            'first_session': self.session_history[0]['timestamp'] if self.session_history else None,
            'last_session': self.session_history[-1]['timestamp'] if self.session_history else None
        }
    
    def export_analytics_data(self, filename: str = None) -> str:
        """Export all analytics data to JSON"""
        if not filename:
            filename = f"symptom_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        analytics_data = {
            'session_history': self.session_history,
            'statistics': self.get_session_statistics(),
            'export_timestamp': datetime.now().isoformat(),
            'total_sessions': len(self.session_history)
        }
        
        with open(filename, 'w') as f:
            json.dump(analytics_data, f, indent=2, default=str)
        
        return filename
    
    def load_analytics_data(self, filename: str):
        """Load analytics data from JSON file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            self.session_history = data.get('session_history', [])
            
            # Rebuild symptom trends
            self.symptom_trends = defaultdict(list)
            for session in self.session_history:
                for symptom, severity in session.get('symptoms', {}).items():
                    self.symptom_trends[symptom].append({
                        'timestamp': session['timestamp'],
                        'severity': severity,
                        'session_id': session.get('session_id', 0)
                    })
            
            return True
        except Exception as e:
            print(f"Error loading analytics data: {e}")
            return False

# Create global analytics instance
analytics = SymptomAnalytics()
