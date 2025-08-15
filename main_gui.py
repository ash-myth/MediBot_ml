"""
Advanced Symptom Checker Chatbot GUI
Modern interface with chat capabilities and symptom assessment
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import json
from datetime import datetime
import threading
from typing import Dict, List
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from symptom_database import symptom_db
try:
    from ml_analyzer import ml_analyzer
    ML_ENABLED = True
    print("✅ ML Analyzer loaded successfully!")
except ImportError as e:
    print(f"⚠️ ML Analyzer not available: {e}")
    ML_ENABLED = False

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SymptomCheckerGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Advanced Symptom Checker Chatbot")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Initialize data storage
        self.current_symptoms = {}
        self.conversation_history = []
        self.current_assessment = {}
        self.user_profile = {}
        
        # Audience (Patient or Clinician)
        self.audience = "Patient"
        
        # Create main layout
        self.create_main_layout()
        self.create_chat_interface()
        self.create_symptom_panel()
        self.create_results_panel()
        self.create_menu_bar()
        
        # Initialize chatbot
        self.chatbot_active = False
        self.current_question_index = 0
        self.follow_up_questions = []
        
        # Welcome message with medical disclaimer
        welcome_msg = ("Hello! I'm your advanced symptom checker assistant. I can help you assess your symptoms and provide general health guidance.\n\n"
                      "⚠️ IMPORTANT MEDICAL DISCLAIMER: This tool is for informational purposes only and is NOT a substitute for professional medical advice, diagnosis, or treatment. "
                      "Always consult qualified healthcare professionals for medical concerns. In emergencies, call 102 immediately.\n\n"
                      "How are you feeling today?")
        self.add_bot_message(welcome_msg)
    
    def create_main_layout(self):
        """Create the main layout structure"""
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=2)  # Chat area
        self.root.grid_columnconfigure(1, weight=1)  # Side panel
        self.root.grid_rowconfigure(0, weight=1)
        
        # Main chat frame
        self.chat_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.chat_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        self.chat_frame.grid_columnconfigure(0, weight=1)
        self.chat_frame.grid_rowconfigure(1, weight=1)
        
        # Side panel frame
        self.side_panel = ctk.CTkFrame(self.root, corner_radius=15)
        self.side_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
    
    def create_chat_interface(self):
        """Create the chat interface"""
        # Chat header
        header_frame = ctk.CTkFrame(self.chat_frame, height=60, corner_radius=10)
        header_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Bot avatar (using emoji for simplicity)
        bot_avatar = ctk.CTkLabel(header_frame, text="🤖", font=ctk.CTkFont(size=24))
        bot_avatar.grid(row=0, column=0, padx=15, pady=15)
        
        # Header text
        header_label = ctk.CTkLabel(
            header_frame, 
            text="Symptom Checker Assistant", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        header_label.grid(row=0, column=1, padx=15, pady=15, sticky="w")
        
        # Status indicator
        self.status_label = ctk.CTkLabel(
            header_frame, 
            text="● Online", 
            font=ctk.CTkFont(size=12),
            text_color="green"
        )
        self.status_label.grid(row=0, column=2, padx=15, pady=15)
        
        # Chat display area
        self.chat_display = ctk.CTkScrollableFrame(
            self.chat_frame, 
            corner_radius=10,
            fg_color=("gray95", "gray10")
        )
        self.chat_display.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        self.chat_display.grid_columnconfigure(0, weight=1)
        
        # Input area
        input_frame = ctk.CTkFrame(self.chat_frame, height=80, corner_radius=10)
        input_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 15))
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Text input
        self.text_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="Type your message or describe your symptoms...",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.text_input.grid(row=0, column=0, sticky="ew", padx=15, pady=20)
        self.text_input.bind("<Return>", self.send_message)
        
        # Send button
        self.send_button = ctk.CTkButton(
            input_frame,
            text="Send",
            width=80,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.send_message
        )
        self.send_button.grid(row=0, column=1, padx=(5, 15), pady=20)
        
        # Quick action buttons
        quick_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        quick_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 15))
        
        quick_buttons = [
            ("🌡️ Fever", lambda: self.quick_symptom("fever")),
            ("😷 Cough", lambda: self.quick_symptom("cough")),
            ("🤕 Headache", lambda: self.quick_symptom("headache")),
            ("😵 Nausea", lambda: self.quick_symptom("nausea"))
        ]
        
        for i, (text, command) in enumerate(quick_buttons):
            btn = ctk.CTkButton(
                quick_frame,
                text=text,
                width=100,
                height=30,
                font=ctk.CTkFont(size=12),
                command=command
            )
            btn.grid(row=0, column=i, padx=5, pady=5)
    
    def create_symptom_panel(self):
        """Create the symptom tracking panel"""
        # Symptoms section
        symptoms_label = ctk.CTkLabel(
            self.side_panel,
            text="Current Symptoms",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        symptoms_label.pack(pady=(20, 10), padx=20)
        
        # Symptoms frame
        self.symptoms_frame = ctk.CTkScrollableFrame(
            self.side_panel,
            height=200,
            corner_radius=10
        )
        self.symptoms_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Add symptom button
        add_symptom_btn = ctk.CTkButton(
            self.side_panel,
            text="+ Add Symptom",
            height=35,
            font=ctk.CTkFont(size=14),
            command=self.show_symptom_selector
        )
        add_symptom_btn.pack(fill="x", padx=20, pady=(0, 20))
        
        # Severity assessment
        severity_label = ctk.CTkLabel(
            self.side_panel,
            text="Overall Severity",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        severity_label.pack(pady=(0, 10), padx=20)
        
        self.severity_bar = ctk.CTkProgressBar(self.side_panel, width=200)
        self.severity_bar.pack(padx=20, pady=(0, 10))
        self.severity_bar.set(0)
        
        self.severity_text = ctk.CTkLabel(
            self.side_panel,
            text="No symptoms recorded",
            font=ctk.CTkFont(size=12)
        )
        self.severity_text.pack(padx=20, pady=(0, 20))
    
    def create_results_panel(self):
        """Create the results and recommendations panel"""
        # Results section
        results_label = ctk.CTkLabel(
            self.side_panel,
            text="Assessment Results",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        results_label.pack(pady=(0, 10), padx=20)
        
        # Results frame
        self.results_frame = ctk.CTkScrollableFrame(
            self.side_panel,
            height=150,
            corner_radius=10
        )
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Action buttons
        button_frame = ctk.CTkFrame(self.side_panel, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.export_btn = ctk.CTkButton(
            button_frame,
            text="📄 Export Report",
            height=35,
            font=ctk.CTkFont(size=12),
            command=self.export_report
        )
        self.export_btn.pack(fill="x", pady=(0, 10))
        
        self.clear_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Clear All",
            height=35,
            font=ctk.CTkFont(size=12),
            fg_color="red",
            hover_color="darkred",
            command=self.clear_all_data
        )
        self.clear_btn.pack(fill="x")
    
    def create_menu_bar(self):
        """Create menu bar with additional options"""
        # Since CustomTkinter doesn't have native menu bar, create a frame
        menu_frame = ctk.CTkFrame(self.root, height=40, corner_radius=0)
        menu_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 0))
        
        # Menu buttons
        menu_buttons = [
            ("Settings ⚙️", self.open_settings),
            ("History 📋", self.show_history),
            ("Help ❓", self.show_help),
            ("About ℹ️", self.show_about)
        ]
        
        for i, (text, command) in enumerate(menu_buttons):
            btn = ctk.CTkButton(
                menu_frame,
                text=text,
                width=100,
                height=30,
                font=ctk.CTkFont(size=11),
                command=command
            )
            btn.pack(side="left", padx=5, pady=5)
    
    def add_message_bubble(self, message: str, is_user: bool = True, timestamp: str = None):
        """Add a message bubble to the chat display"""
        if timestamp is None:
            timestamp = datetime.now().strftime("%H:%M")
        
        # Message container
        msg_frame = ctk.CTkFrame(self.chat_display, fg_color="transparent")
        msg_frame.grid(sticky="ew", padx=10, pady=5)
        msg_frame.grid_columnconfigure(0, weight=1)
        
        # Message bubble
        if is_user:
            bubble_color = ("#3B82F6", "#1E40AF")
            text_color = "white"
            anchor = "e"
            padx = (50, 10)
        else:
            bubble_color = ("#E5E7EB", "#374151")
            text_color = ("black", "white")
            anchor = "w"
            padx = (10, 50)
        
        bubble = ctk.CTkFrame(msg_frame, fg_color=bubble_color, corner_radius=15)
        bubble.grid(sticky=anchor, padx=padx, pady=2)
        
        # Message text with better formatting
        # Break long messages into paragraphs for better readability
        formatted_message = self._format_message_for_display(message)
        
        msg_label = ctk.CTkLabel(
            bubble,
            text=formatted_message,
            font=ctk.CTkFont(size=13),
            text_color=text_color,
            wraplength=450,  # Increased for better text flow
            justify="left"
        )
        msg_label.pack(padx=15, pady=10)
        
        # Timestamp
        time_label = ctk.CTkLabel(
            msg_frame,
            text=timestamp,
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        time_label.grid(sticky=anchor, padx=padx, pady=(0, 5))
        
        # Scroll to bottom
        self.root.after(100, self._scroll_to_bottom)
    
    def _format_message_for_display(self, message: str) -> str:
        """Format long messages for better readability"""
        # If message is very long, add line breaks at sentence boundaries for better flow
        if len(message) > 200:
            # Split at sentence boundaries and rejoin with better spacing
            sentences = message.replace('. ', '.\n\n').replace('! ', '!\n\n').replace('? ', '?\n\n')
            # Remove excessive line breaks
            formatted = sentences.replace('\n\n\n', '\n\n')
            return formatted
        return message
    
    def _scroll_to_bottom(self):
        """Scroll chat display to bottom"""
        self.chat_display._parent_canvas.yview_moveto(1.0)
    
    def add_bot_message(self, message: str):
        """Add a bot message to the chat"""
        self.add_message_bubble(message, is_user=False)
        self.conversation_history.append({
            "type": "bot",
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
    
    def add_user_message(self, message: str):
        """Add a user message to the chat"""
        self.add_message_bubble(message, is_user=True)
        self.conversation_history.append({
            "type": "user",
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
    
    def send_message(self, event=None):
        """Send user message and process response"""
        message = self.text_input.get().strip()
        if not message:
            return
        
        # Clear input
        self.text_input.delete(0, "end")
        
        # Add user message
        self.add_user_message(message)
        
        # Process message in separate thread to avoid blocking GUI
        threading.Thread(target=self.process_user_message, args=(message,), daemon=True).start()
    
    def process_user_message(self, message: str):
        """Process user message and generate response"""
        # Simulate processing delay
        self.root.after(500, lambda: self._generate_bot_response(message))
    
    def _generate_bot_response(self, message: str):
        """Generate bot response based on user input with ML enhancement"""
        message_lower = message.lower()
        
        # Check for greetings (match whole words to avoid false positives like 'hi' in 'shivery')
        import re
        greeting_patterns = [r"\bhello\b", r"\bhi\b", r"\bhey\b", r"\bgood\s+morning\b", r"\bgood\s+afternoon\b"]
        if any(re.search(pat, message_lower) for pat in greeting_patterns):
            response = "Hello! I'm here to help you with your health concerns. Please tell me about any symptoms you're experiencing."
        
        # Check if this is a detailed description that might benefit from ML analysis
        elif len(message.split()) > 10 and ML_ENABLED:  # Long descriptive message
            # Use ML analysis for comprehensive symptom descriptions
            self._process_with_ml_analysis(message)
            return  # ML processing will handle the response
        
        # Enhanced symptom detection (fallback/simple cases)
        else:
            detected_symptoms = self._detect_symptoms_in_message(message_lower)
            
            if detected_symptoms:
                # Add symptoms and determine severity
                new_symptoms = []
                for symptom in detected_symptoms:
                    if symptom not in self.current_symptoms:
                        # Detect severity from context
                        severity = self._detect_severity_in_message(message_lower)
                        self.current_symptoms[symptom] = severity
                        new_symptoms.append(symptom)
                
                if new_symptoms:
                    self.update_symptom_display()
                    
                    # Generate appropriate response
                    symptom_names = [s.replace('_', ' ').title() for s in new_symptoms]
                    
                    if len(new_symptoms) == 1:
                        response = f"I understand you're experiencing {symptom_names[0]}. "
                        # Add follow-up question
                        questions = symptom_db.get_follow_up_questions(new_symptoms[0])
                        if questions:
                            response += f"{questions[0]}"
                        else:
                            response += "Can you tell me more about this symptom?"
                    else:
                        response = f"I see you're experiencing multiple symptoms: {', '.join(symptom_names)}. "
                        response += "Let me ask some follow-up questions to better understand your condition."
                    
                    self.generate_assessment()
                else:
                    response = "I've noted these symptoms. Is there anything else you'd like to tell me about how you're feeling?"
            
            # Check for symptom severity responses
            elif any(severity in message_lower for severity in ["mild", "moderate", "severe", "light", "heavy", "intense"]):
                if self.current_symptoms:
                    # Update severity for last added symptom
                    last_symptom = list(self.current_symptoms.keys())[-1]
                    if "mild" in message_lower or "light" in message_lower:
                        self.current_symptoms[last_symptom] = "mild"
                    elif "severe" in message_lower or "intense" in message_lower or "heavy" in message_lower:
                        self.current_symptoms[last_symptom] = "severe"
                    else:
                        self.current_symptoms[last_symptom] = "moderate"
                    
                    self.update_symptom_display()
                    self.generate_assessment()
                    response = "Thank you for clarifying the severity. Is there anything else you'd like to tell me about your symptoms?"
                else:
                    response = "I understand. Can you please describe your symptoms in more detail?"
            
            # Default response
            else:
                response = "I understand. Can you please describe your symptoms in more detail? For example, you might say 'I have a headache and feel nauseous' or use the quick buttons below."
        
        self.add_bot_message(response)
    
    def _detect_symptoms_in_message(self, message_lower: str) -> List[str]:
        """Enhanced symptom detection using multiple matching strategies"""
        detected_symptoms = []
        
        # Extended symptom mapping for better detection
        symptom_aliases = {
            "fever": ["fever", "high temperature", "hot", "burning up", "febrile", "high fever", "temperature"],
            "headache": ["headache", "head pain", "head ache", "migraine", "head hurt"],
            "cough": ["cough", "coughing", "hacking", "dry cough", "wet cough", "sore throat", "throat"],
            "nausea": ["nausea", "nauseous", "sick", "queasy", "upset stomach", "feel sick"],
            "fatigue": ["tired", "fatigue", "exhausted", "weakness", "weak", "drained", "worn out"],
            "muscle_pain": ["body aches", "muscle pain", "aches", "sore muscles", "body pain", "muscle aches"],
            "joint_pain": ["joint pain", "joint aches", "stiff joints", "arthritis"],
            "chills": ["chills", "shivering", "cold", "shaking"],
            "dizziness": ["dizzy", "dizziness", "lightheaded", "vertigo", "spinning"],
            "shortness_of_breath": ["shortness of breath", "can't breathe", "breathing problems", "winded"],
            "chest_pain": ["chest pain", "chest hurt", "heart pain", "chest pressure"],
            "abdominal_pain": ["stomach pain", "belly ache", "stomach ache", "gut pain", "abdominal pain"],
            "vomiting": ["vomiting", "throwing up", "puking", "being sick"],
            "diarrhea": ["diarrhea", "loose stools", "runny stools", "frequent bowel movements"]
        }
        
        # Check each symptom and its aliases
        for symptom, aliases in symptom_aliases.items():
            for alias in aliases:
                if alias in message_lower:
                    if symptom not in detected_symptoms:
                        detected_symptoms.append(symptom)
                    break
        
        # Also check database symptoms
        for symptom in symptom_db.get_all_symptoms():
            symptom_readable = symptom.replace("_", " ")
            if symptom_readable in message_lower or symptom in message_lower:
                if symptom not in detected_symptoms:
                    detected_symptoms.append(symptom)
        
        return detected_symptoms
    
    def _detect_severity_in_message(self, message_lower: str) -> str:
        """Detect severity level from message context"""
        # High severity indicators
        severe_indicators = ["severe", "intense", "terrible", "awful", "unbearable", "extreme", "sharp", "high fever"]
        # Low severity indicators
        mild_indicators = ["mild", "slight", "little", "minor", "light", "gentle"]
        
        for indicator in severe_indicators:
            if indicator in message_lower:
                return "severe"
        
        for indicator in mild_indicators:
            if indicator in message_lower:
                return "mild"
        
        return "moderate"  # Default severity
    
    def quick_symptom(self, symptom: str):
        """Add a symptom via quick button"""
        if symptom not in self.current_symptoms:
            self.current_symptoms[symptom] = "moderate"
            self.update_symptom_display()
            
            # Ask follow-up questions
            questions = symptom_db.get_follow_up_questions(symptom)
            if questions:
                self.add_bot_message(f"I see you've selected {symptom.replace('_', ' ')}. {questions[0]}")
                self.follow_up_questions = questions[1:]
            else:
                self.add_bot_message(f"I've noted that you have {symptom.replace('_', ' ')}. Any other symptoms you'd like to mention?")
            
            self.generate_assessment()
    
    def update_symptom_display(self):
        """Update the symptom display panel"""
        # Clear existing symptom widgets
        for widget in self.symptoms_frame.winfo_children():
            widget.destroy()
        
        # Add current symptoms
        for i, (symptom, severity) in enumerate(self.current_symptoms.items()):
            symptom_frame = ctk.CTkFrame(self.symptoms_frame)
            symptom_frame.pack(fill="x", pady=5, padx=5)
            symptom_frame.grid_columnconfigure(0, weight=1)
            
            # Symptom name
            symptom_label = ctk.CTkLabel(
                symptom_frame,
                text=symptom.replace("_", " ").title(),
                font=ctk.CTkFont(size=12, weight="bold")
            )
            symptom_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
            
            # Severity indicator
            severity_colors = {"mild": "green", "moderate": "orange", "severe": "red"}
            severity_label = ctk.CTkLabel(
                symptom_frame,
                text=severity.title(),
                font=ctk.CTkFont(size=11),
                text_color=severity_colors.get(severity, "gray")
            )
            severity_label.grid(row=0, column=1, sticky="e", padx=10, pady=5)
            
            # Remove button
            remove_btn = ctk.CTkButton(
                symptom_frame,
                text="×",
                width=25,
                height=25,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color="red",
                hover_color="darkred",
                command=lambda s=symptom: self.remove_symptom(s)
            )
            remove_btn.grid(row=0, column=2, padx=(5, 10), pady=5)
        
        # Update severity assessment
        self.update_severity_display()
    
    def update_severity_display(self):
        """Update the overall severity display"""
        if not self.current_symptoms:
            self.severity_bar.set(0)
            self.severity_text.configure(text="No symptoms recorded")
            return
        
        # Calculate severity score
        severity_score = symptom_db.calculate_severity_score(self.current_symptoms)
        max_possible_score = len(self.current_symptoms) * 5  # Max weight is 5
        
        if max_possible_score > 0:
            severity_ratio = min(severity_score / max_possible_score, 1.0)
            self.severity_bar.set(severity_ratio)
            
            # Determine severity level
            if severity_ratio < 0.3:
                level = "Mild"
                color = "green"
            elif severity_ratio < 0.7:
                level = "Moderate"
                color = "orange"
            else:
                level = "Severe"
                color = "red"
            
            self.severity_text.configure(
                text=f"{level} ({severity_score}/{max_possible_score})",
                text_color=color
            )
    
    def remove_symptom(self, symptom: str):
        """Remove a symptom from the current list"""
        if symptom in self.current_symptoms:
            del self.current_symptoms[symptom]
            self.update_symptom_display()
            self.generate_assessment()
            self.add_bot_message(f"I've removed {symptom.replace('_', ' ')} from your symptom list.")
    
    def generate_assessment(self):
        """Generate medical assessment based on current symptoms (database-based)"""
        if not self.current_symptoms:
            # Clear results
            for widget in self.results_frame.winfo_children():
                widget.destroy()
            self.severity_bar.set(0)
            self.severity_text.configure(text="No symptoms recorded")
            return
        
        # Get related conditions
        symptom_list = list(self.current_symptoms.keys())
        conditions = symptom_db.get_related_conditions(symptom_list)
        
        # Clear results frame
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Display top conditions
        results_title = ctk.CTkLabel(
            self.results_frame,
            text="Possible Conditions:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        results_title.pack(pady=(10, 5))
        
        for i, (condition, probability) in enumerate(list(conditions.items())[:5]):
            condition_info = symptom_db.get_condition_info(condition)
            if condition_info:
                condition_frame = ctk.CTkFrame(self.results_frame)
                condition_frame.pack(fill="x", pady=5, padx=5)
                
                # Condition name and probability
                name_label = ctk.CTkLabel(
                    condition_frame,
                    text=f"{condition_info.get('name', condition)} ({probability:.1f}%)",
                    font=ctk.CTkFont(size=12, weight="bold")
                )
                name_label.pack(anchor="w", padx=10, pady=(10, 5))
                
                # Description
                desc_label = ctk.CTkLabel(
                    condition_frame,
                    text=condition_info.get('description', ''),
                    font=ctk.CTkFont(size=10),
                    wraplength=200,
                    justify="left"
                )
                desc_label.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Recommendations
        if conditions:
            top_condition = list(conditions.keys())[0]
            condition_info = symptom_db.get_condition_info(top_condition)
            if condition_info and 'recommendations' in condition_info:
                rec_title = ctk.CTkLabel(
                    self.results_frame,
                    text="Recommendations:",
                    font=ctk.CTkFont(size=14, weight="bold")
                )
                rec_title.pack(pady=(20, 5))
                
                for rec in condition_info['recommendations']:
                    rec_label = ctk.CTkLabel(
                        self.results_frame,
                        text=f"• {rec}",
                        font=ctk.CTkFont(size=11),
                        wraplength=200,
                        justify="left"
                    )
                    rec_label.pack(anchor="w", padx=10, pady=2)
        
        # Store current assessment
        self.current_assessment = {
            "symptoms": self.current_symptoms,
            "conditions": conditions,
            "timestamp": datetime.now().isoformat()
        }
    
    def _display_ml_diagnosis(self, diagnosis: Dict):
        """Render ML diagnosis nicely in the results panel"""
        # Clear results frame
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        primary = diagnosis.get('primary_diagnosis', {})
        severity = diagnosis.get('severity_assessment', {})
        detected = diagnosis.get('detected_symptoms', [])
        treatments = diagnosis.get('treatment_recommendations', [])
        remedies = diagnosis.get('home_remedies', [])
        warnings = diagnosis.get('when_to_see_doctor', [])
        
        # Title
        title = ctk.CTkLabel(
            self.results_frame,
            text=f"Primary Assessment: {primary.get('condition', 'Unknown')}",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title.pack(pady=(10, 6), anchor="w", padx=10)
        
        # Probability and severity
        prob_sev = ctk.CTkLabel(
            self.results_frame,
            text=f"Likelihood: {primary.get('confidence', 'n/a').title()} • Severity: {severity.get('level','moderate').title()}",
            font=ctk.CTkFont(size=12)
        )
        prob_sev.pack(pady=(0, 8), anchor="w", padx=10)
        
        # Description
        desc = ctk.CTkLabel(
            self.results_frame,
            text=primary.get('description', ''),
            font=ctk.CTkFont(size=11),
            wraplength=260,
            justify="left"
        )
        desc.pack(pady=(0, 10), anchor="w", padx=10)
        
        # Detected symptoms
        if detected:
            det_text = ctk.CTkLabel(
                self.results_frame,
                text=f"Symptoms detected: {', '.join([s.replace('_',' ').title() for s in detected])}",
                font=ctk.CTkFont(size=11),
                wraplength=260,
                justify="left"
            )
            det_text.pack(pady=(0, 10), anchor="w", padx=10)
        
        # Recommendations
        if treatments:
            rec_title = ctk.CTkLabel(self.results_frame, text="Recommended care:", font=ctk.CTkFont(size=12, weight="bold"))
            rec_title.pack(pady=(0, 4), anchor="w", padx=10)
            for t in treatments[:6]:
                rec = ctk.CTkLabel(self.results_frame, text=f"• {t}", font=ctk.CTkFont(size=11), wraplength=260, justify="left")
                rec.pack(anchor="w", padx=16)
        
        if remedies:
            rem_title = ctk.CTkLabel(self.results_frame, text="Helpful home remedies:", font=ctk.CTkFont(size=12, weight="bold"))
            rem_title.pack(pady=(8, 4), anchor="w", padx=10)
            for r in remedies[:4]:
                rem = ctk.CTkLabel(self.results_frame, text=f"• {r}", font=ctk.CTkFont(size=11), wraplength=260, justify="left")
                rem.pack(anchor="w", padx=16)
        
        if warnings:
            warn_title = ctk.CTkLabel(self.results_frame, text="Seek medical care if:", font=ctk.CTkFont(size=12, weight="bold"))
            warn_title.pack(pady=(8, 4), anchor="w", padx=10)
            for w in warnings[:5]:
                wr = ctk.CTkLabel(self.results_frame, text=f"• {w}", font=ctk.CTkFont(size=11), wraplength=260, justify="left")
                wr.pack(anchor="w", padx=16)
        
        # Update severity bar
        sev_map = {"mild": 0.3, "moderate": 0.6, "severe": 0.9}
        ratio = sev_map.get(severity.get('level', 'moderate'), 0.6)
        self.severity_bar.set(ratio)
        level = severity.get('level', 'moderate').title()
        color = "green" if level.lower()=="mild" else "orange" if level.lower()=="moderate" else "red"
        self.severity_text.configure(text=f"{level}", text_color=color)
    
    def show_symptom_selector(self):
        """Show symptom selector dialog"""
        selector_window = ctk.CTkToplevel(self.root)
        selector_window.title("Select Symptoms")
        selector_window.geometry("500x600")
        selector_window.transient(self.root)
        selector_window.grab_set()
        
        # Search entry
        search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            selector_window,
            textvariable=search_var,
            placeholder_text="Search symptoms...",
            height=40
        )
        search_entry.pack(fill="x", padx=20, pady=20)
        
        # Symptoms list
        symptoms_list = ctk.CTkScrollableFrame(selector_window)
        symptoms_list.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        def update_symptoms_list():
            # Clear existing
            for widget in symptoms_list.winfo_children():
                widget.destroy()
            
            search_term = search_var.get().lower()
            all_symptoms = symptom_db.get_all_symptoms()
            
            for symptom in all_symptoms:
                display_name = symptom.replace("_", " ").title()
                if not search_term or search_term in display_name.lower():
                    symptom_frame = ctk.CTkFrame(symptoms_list)
                    symptom_frame.pack(fill="x", pady=5, padx=5)
                    
                    symptom_label = ctk.CTkLabel(
                        symptom_frame,
                        text=display_name,
                        font=ctk.CTkFont(size=12)
                    )
                    symptom_label.pack(side="left", padx=15, pady=10)
                    
                    add_btn = ctk.CTkButton(
                        symptom_frame,
                        text="Add",
                        width=60,
                        height=30,
                        command=lambda s=symptom: self.add_selected_symptom(s, selector_window)
                    )
                    add_btn.pack(side="right", padx=15, pady=10)
        
        search_var.trace("w", lambda *args: update_symptoms_list())
        update_symptoms_list()
    
    def _process_with_ml_analysis(self, message: str):
        """Process complex symptom description using ML analysis"""
        try:
            # Show processing message
            self.add_bot_message("🤖 Analyzing your symptoms using advanced AI... Please wait a moment.")
            
            # First check the raw ML analysis for emergency conditions
            ml_results = ml_analyzer.analyze_description(message)
            
            # CRITICAL: Check for emergency first - highest priority
            if "emergency" in ml_results and ml_results["emergency"]:
                # Emergency detected - immediate response required
                emergency_message = ml_results["message"]
                self.add_bot_message(emergency_message)
                
                # Update severity to critical
                self.severity_bar.set(1.0)
                self.severity_text.configure(text="EMERGENCY - CALL 102", text_color="red")
                
                # Add emergency symptoms to display 
                if "extracted_symptoms" in ml_results:
                    for symptom in ml_results["extracted_symptoms"]:
                        symptom_key = symptom.lower().replace(' ', '_').replace('-', '_')
                        self.current_symptoms[symptom_key] = "severe"
                
                self.update_symptom_display()
                
                # Clear results panel and show emergency message
                for widget in self.results_frame.winfo_children():
                    widget.destroy()
                    
                emergency_label = ctk.CTkLabel(
                    self.results_frame,
                    text="🚨 MEDICAL EMERGENCY\n\nCALL EMERGENCY SERVICES\nIMMEDIATELY",
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color="red",
                    justify="center"
                )
                emergency_label.pack(pady=20, padx=10)
                
                return  # Stop processing - emergency takes priority
            
            # Use ML analyzer for comprehensive analysis (text + structured diagnosis)
            analysis_result = ml_analyzer.analyze_symptoms(message)
            diagnosis = ml_analyzer.get_comprehensive_diagnosis(message)
            
            if analysis_result:
                # Extract detected symptoms and add to current symptoms
                detected_symptoms = analysis_result.get('symptoms', [])
                predicted_severity = analysis_result.get('severity', 'moderate')
                
                # Add detected symptoms
                new_symptoms = []
                for symptom in detected_symptoms:
                    # Convert symptom name to match our database format
                    symptom_key = symptom.lower().replace(' ', '_').replace('-', '_')
                    if symptom_key not in self.current_symptoms:
                        self.current_symptoms[symptom_key] = predicted_severity
                        new_symptoms.append(symptom)
                
                # Update display if new symptoms found
                if new_symptoms:
                    self.update_symptom_display()
                
                # Show ML diagnosis in the results panel (more human-friendly)
                if diagnosis and 'primary_diagnosis' in diagnosis:
                    self._display_ml_diagnosis(diagnosis)
                else:
                    # Fall back to legacy assessment if no diagnosis
                    self.generate_assessment()
                
                # Generate role-based response (Patient vs Clinician)
                try:
                    role_response = ml_analyzer.generate_response_for_audience(diagnosis, self.audience)
                    if role_response:
                        self.add_bot_message(role_response)
                    else:
                        # Fallback to generic response
                        response = analysis_result.get('response', '')
                        if response:
                            self.add_bot_message(response)
                except Exception:
                    response = analysis_result.get('response', '')
                    if response:
                        self.add_bot_message(response)
                else:
                    # Fallback response
                    if new_symptoms:
                        symptom_list = ', '.join(new_symptoms)
                        self.add_bot_message(f"Based on your description, I've identified the following symptoms: {symptom_list}. I've analyzed your condition and provided recommendations in the results panel.")
                    else:
                        self.add_bot_message("I've analyzed your description. Please check the results panel for my assessment and recommendations.")
            else:
                # Fallback to regular processing if ML analysis fails
                self.add_bot_message("I understand your description. Let me analyze this using our standard assessment method.")
                self._generate_standard_response(message)
                
        except Exception as e:
            print(f"ML Analysis error: {e}")
            self.add_bot_message("I encountered an issue with the advanced analysis. Let me help you with the standard assessment method.")
            self._generate_standard_response(message)
    
    def _generate_standard_response(self, message: str):
        """Generate standard response when ML is not available"""
        message_lower = message.lower()
        detected_symptoms = self._detect_symptoms_in_message(message_lower)
        
        if detected_symptoms:
            # Add symptoms and determine severity
            new_symptoms = []
            for symptom in detected_symptoms:
                if symptom not in self.current_symptoms:
                    severity = self._detect_severity_in_message(message_lower)
                    self.current_symptoms[symptom] = severity
                    new_symptoms.append(symptom)
            
            if new_symptoms:
                self.update_symptom_display()
                self.generate_assessment()
                
                symptom_names = [s.replace('_', ' ').title() for s in new_symptoms]
                response = f"I've identified these symptoms from your description: {', '.join(symptom_names)}. Please let me know if you'd like to add any additional details or other symptoms."
                self.add_bot_message(response)
            else:
                self.add_bot_message("I've noted your description. Is there anything specific you'd like me to focus on?")
        else:
            self.add_bot_message("Thank you for the detailed description. Could you help me identify specific symptoms you're experiencing? For example, fever, headache, nausea, etc.")
    
    def add_selected_symptom(self, symptom: str, window):
        """Add selected symptom and close selector"""
        if symptom not in self.current_symptoms:
            self.current_symptoms[symptom] = "moderate"
            self.update_symptom_display()
            self.generate_assessment()
            
            # Ask about severity
            self.add_bot_message(f"I've added {symptom.replace('_', ' ')} to your symptoms. How would you rate its severity: mild, moderate, or severe?")
        
        window.destroy()
    
    def export_report(self):
        """Export current assessment as a report"""
        if not self.current_assessment:
            messagebox.showwarning("No Data", "No assessment data available to export.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                report_data = {
                    "timestamp": datetime.now().isoformat(),
                    "symptoms": self.current_symptoms,
                    "assessment": self.current_assessment,
                    "conversation_history": self.conversation_history
                }
                
                with open(file_path, 'w') as f:
                    json.dump(report_data, f, indent=2)
                
                messagebox.showinfo("Export Successful", f"Report exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export report: {str(e)}")
    
    def clear_all_data(self):
        """Clear all current data"""
        if messagebox.askyesno("Clear All Data", "Are you sure you want to clear all symptoms and conversation history?"):
            self.current_symptoms = {}
            self.conversation_history = []
            self.current_assessment = {}
            self.follow_up_questions = []
            
            # Clear displays
            self.update_symptom_display()
            for widget in self.chat_display.winfo_children():
                widget.destroy()
            for widget in self.results_frame.winfo_children():
                widget.destroy()
            
            # Welcome message
            self.add_bot_message("Hello! I'm ready to help you with a fresh start. How are you feeling today?")
    
    def open_settings(self):
        """Open settings dialog"""
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Theme selection
        theme_label = ctk.CTkLabel(settings_window, text="Theme:", font=ctk.CTkFont(size=14, weight="bold"))
        theme_label.pack(pady=(20, 10))
        
        theme_var = ctk.StringVar(value="dark")
        theme_menu = ctk.CTkOptionMenu(
            settings_window,
            variable=theme_var,
            values=["dark", "light", "system"],
            command=lambda choice: ctk.set_appearance_mode(choice)
        )
        theme_menu.pack(pady=(0, 20))
        
        # Audience selection
        audience_label = ctk.CTkLabel(settings_window, text="Audience:", font=ctk.CTkFont(size=14, weight="bold"))
        audience_label.pack(pady=(0, 10))
        
        audience_var = ctk.StringVar(value=self.audience)
        def set_audience(choice):
            self.audience = choice
        audience_menu = ctk.CTkOptionMenu(
            settings_window,
            variable=audience_var,
            values=["Patient", "Clinician"],
            command=set_audience
        )
        audience_menu.pack(pady=(0, 20))
        
        # Close button
        close_btn = ctk.CTkButton(
            settings_window,
            text="Close",
            command=settings_window.destroy
        )
        close_btn.pack(pady=20)
    
    def show_history(self):
        """Show conversation history"""
        history_window = ctk.CTkToplevel(self.root)
        history_window.title("Conversation History")
        history_window.geometry("600x500")
        history_window.transient(self.root)
        
        history_text = ctk.CTkTextbox(history_window)
        history_text.pack(fill="both", expand=True, padx=20, pady=20)
        
        for entry in self.conversation_history:
            timestamp = datetime.fromisoformat(entry["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
            sender = "You" if entry["type"] == "user" else "Bot"
            history_text.insert("end", f"[{timestamp}] {sender}: {entry['message']}\n\n")
    
    def show_help(self):
        """Show help dialog"""
        ml_status = "✅ Available" if ML_ENABLED else "⚠️ Not Available"
        help_text = f"""
        Advanced Symptom Checker Chatbot Help
        
        How to use:
        1. Describe your symptoms in natural language in the chat box
        2. For complex descriptions (flu symptoms, etc.), the AI will analyze automatically
        3. Use quick buttons for common symptoms
        4. Answer follow-up questions for better assessment
        5. Review results in the side panel
        6. Export reports for your records
        
        Features:
        • Enhanced ML-powered symptom analysis {ml_status}
        • Natural language understanding
        • Medical condition suggestions with probabilities
        • Severity assessment and scoring
        • Treatment and prevention recommendations
        • Export functionality (JSON format)
        • Complete conversation history
        • Modern, user-friendly interface
        
        Advanced Features:
        • Supports complex symptom descriptions
        • Intelligent symptom extraction from text
        • Machine learning disease prediction
        • Comprehensive medical knowledge base
        
        Tips:
        • Try describing symptoms like "I have flu-like symptoms with high fever and body aches"
        • The longer and more detailed your description, the better the analysis
        • Use natural language - no need for medical terminology
        
        Disclaimer:
        This tool is for informational purposes only and uses AI for analysis.
        Always consult qualified healthcare professionals for medical advice.
        Do not rely solely on this tool for medical decisions.
        """
        
        messagebox.showinfo("Help", help_text)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
        Advanced Symptom Checker Chatbot
        Version 1.0
        
        A modern, AI-powered symptom assessment tool
        with an intuitive chat interface.
        
        Features advanced medical database and
        intelligent condition matching algorithms.
        
        Developed with CustomTkinter for
        a modern, user-friendly experience.
        """
        
        messagebox.showinfo("About", about_text)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = SymptomCheckerGUI()
    app.run()
