# 📖 User Guide - Advanced Symptom Checker Chatbot

Welcome to your comprehensive guide for using the Advanced Symptom Checker Chatbot! This guide will walk you through every feature and help you get the most out of this health assessment tool.

## 🚀 Getting Started

### First Launch
1. **Start the Application**
   - Double-click the desktop shortcut (Windows)
   - Or run `python main_gui.py` from the installation folder
   - The application will open with a modern dark interface

2. **Initial Welcome**
   - You'll see the chatbot greet you with a welcome message
   - The interface consists of three main areas:
     - **Chat Area (Left)**: Main conversation interface
     - **Symptoms Panel (Right Top)**: Current symptoms tracking
     - **Results Panel (Right Bottom)**: Assessment results and recommendations

## 💬 Using the Chat Interface

### Basic Conversation
The chatbot understands natural language. Here are some effective ways to communicate:

#### ✅ Good Examples:
- "I have a severe headache on the left side of my head"
- "I've been feeling nauseous for the past 2 days"
- "I have chest pain that gets worse when I breathe deeply"
- "My fever started yesterday and I feel very weak"

#### ❌ Less Effective Examples:
- "I don't feel good"
- "Something's wrong"
- "Help" (without specifics)

### Quick Action Buttons
Use the quick buttons below the chat input for common symptoms:

| Button | Purpose | What It Does |
|--------|---------|--------------|
| 🌡️ **Fever** | Log fever symptoms | Adds fever to your symptom list |
| 😷 **Cough** | Record cough details | Starts cough assessment |
| 🤕 **Headache** | Track headache patterns | Begins headache evaluation |
| 😵 **Nausea** | Monitor nausea episodes | Logs nausea symptoms |

### Advanced Input Techniques

#### Severity Descriptions
The chatbot understands various severity levels:
- **Mild**: "slight", "minor", "barely noticeable", "light"
- **Moderate**: "medium", "average", "noticeable", "regular"  
- **Severe**: "intense", "terrible", "unbearable", "extreme", "sharp"

#### Duration Information
Specify how long you've had symptoms:
- "for 3 hours"
- "since yesterday"
- "for the past week"
- "started 2 days ago"

#### Location Specificity
Be specific about where symptoms occur:
- "left side of my chest"
- "back of my head"
- "upper abdomen"
- "right shoulder"

## 📊 Understanding the Symptoms Panel

### Current Symptoms Display
Each symptom in your list shows:
- **Name**: The symptom type (e.g., "Headache", "Fever")
- **Severity**: Color-coded indicator (Green=Mild, Orange=Moderate, Red=Severe)
- **Remove Button (×)**: Click to remove the symptom

### Severity Assessment
- **Progress Bar**: Shows overall symptom severity
- **Score**: Numerical representation of your symptoms
- **Level**: Text description (Mild/Moderate/Severe)

### Adding Symptoms Manually
1. Click **"+ Add Symptom"** button
2. Search for symptoms in the dialog box
3. Click **"Add"** next to desired symptoms
4. The chatbot will ask follow-up questions about severity

## 🔍 Assessment Results Panel

### Possible Conditions
The results panel displays:
- **Condition Names**: Medical conditions that match your symptoms
- **Probability Percentages**: Likelihood based on symptom patterns
- **Descriptions**: Brief explanation of each condition
- **Ranking**: Ordered by probability (highest first)

### Medical Recommendations
For the most likely condition, you'll see:
- **Immediate Actions**: What to do right away
- **When to Seek Care**: Guidance on medical consultation
- **Self-Care Tips**: How to manage symptoms at home
- **Warning Signs**: When to seek emergency care

## 🎯 Advanced Features

### Export Functionality
Save your assessment for medical consultations:

1. **Click "📄 Export Report"**
2. **Choose File Format**:
   - **JSON**: Machine-readable data for analysis
   - **Text**: Human-readable format for sharing
3. **Save Location**: Choose where to save the file
4. **Use the Report**: Share with healthcare providers

### Conversation History
Access your chat history:
1. Click **"History 📋"** in the menu bar
2. Review all previous conversations
3. Use for tracking symptom patterns over time

### Settings Customization
Personalize your experience:
1. Click **"Settings ⚙️"** in the menu bar
2. **Theme Options**:
   - **Dark**: Default modern dark theme
   - **Light**: Clean light interface
   - **System**: Follows your OS theme

### Clear All Data
Reset the application:
1. Click **"🗑️ Clear All"** button
2. Confirm you want to clear all data
3. All symptoms and chat history will be removed

## 📈 Analytics and Tracking

### Session Tracking
The app automatically tracks:
- **Symptom Frequency**: How often symptoms occur
- **Severity Patterns**: Changes in symptom severity
- **Condition Assessments**: Historical diagnosis patterns
- **Time Trends**: When symptoms typically occur

### Visual Analytics
Generate charts and visualizations:
- **Symptom Frequency Charts**: Most common symptoms
- **Severity Distribution**: Breakdown of severity levels
- **Timeline Analysis**: Symptom patterns over time
- **Condition Probability Charts**: Assessment accuracy

## ⚠️ Safety Guidelines

### When to Seek Immediate Medical Attention
**Call Emergency Services (911/999/112) if experiencing:**
- Severe chest pain or pressure
- Difficulty breathing or shortness of breath
- Signs of stroke (face drooping, arm weakness, speech difficulty)
- Severe allergic reactions
- Loss of consciousness
- Severe bleeding or trauma
- Suicidal thoughts

### High Priority Symptoms
**Contact Healthcare Provider Within 24 Hours:**
- Persistent high fever (>101.3°F/38.5°C)
- Severe abdominal pain
- Persistent vomiting
- Signs of dehydration
- Worsening symptoms
- Symptoms that don't improve with rest

### Important Reminders
- ✅ This tool is for **information only**
- ✅ Always consult healthcare professionals for medical advice
- ✅ Never delay seeking care based on this assessment
- ✅ Trust your instincts - if something feels seriously wrong, seek help

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Application Won't Start
**Solutions:**
1. Check Python is installed (version 3.8+)
2. Verify all packages are installed: `pip install -r requirements.txt`
3. Try running: `python -m tkinter` to test GUI support
4. On Linux: `sudo apt-get install python3-tk`

#### Chat Not Responding
**Solutions:**
1. Check for error messages in the chat
2. Restart the application
3. Clear conversation history via Settings
4. Try simpler, more direct symptom descriptions

#### Charts Not Generating
**Solutions:**
1. Ensure matplotlib is installed: `pip show matplotlib`
2. Check file permissions in the application folder
3. Try closing other applications to free memory

#### Slow Performance
**Solutions:**
1. Close other applications to free RAM
2. Clear conversation history
3. Switch to light theme mode
4. Restart the application

### Getting Additional Help

#### Built-in Help
- Click **"Help ❓"** in the menu bar for quick guidance
- Click **"About ℹ️"** for version and system information

#### Documentation
- Refer to `README.md` for technical details
- Check system requirements and compatibility

#### Reporting Issues
If you encounter bugs or problems:
1. Note what you were doing when the issue occurred
2. Check if the issue is reproducible
3. Look for any error messages
4. Consider reporting via GitHub issues (if applicable)

## 🎓 Tips for Best Results

### Effective Communication
1. **Be Specific**: "Sharp chest pain on the left side" vs. "chest hurts"
2. **Include Context**: Mention when symptoms started, what makes them better/worse
3. **Use Natural Language**: The AI understands conversational English
4. **Answer Follow-ups**: Respond to the chatbot's clarifying questions

### Symptom Tracking
1. **Regular Updates**: Use the app consistently for better pattern recognition
2. **Honest Assessment**: Rate severity accurately, don't minimize serious symptoms
3. **Complete Information**: Include all symptoms, even seemingly minor ones
4. **Track Changes**: Note if symptoms improve or worsen

### Medical Consultation Preparation
1. **Export Reports**: Bring printed summaries to appointments
2. **Track Patterns**: Use the analytics to identify trends
3. **Note Questions**: Write down concerns that arise during assessment
4. **Medication Lists**: Keep track of current medications and supplements

## 🔄 Updates and Maintenance

### Keeping the App Updated
- Check for new versions periodically
- Update Python packages: `pip install --upgrade -r requirements.txt`
- Review new features in release notes

### Data Management
- **Backup Important Data**: Export assessments regularly
- **Privacy**: All data stays on your local computer
- **Storage**: Exported files can be saved anywhere you choose

---

## 📞 Emergency Contacts

**Always have these readily available:**
- **Emergency Services**: 911 (US), 999 (UK), 112 (EU)
- **Your Doctor**: Primary care physician contact
- **Pharmacy**: For medication questions
- **Poison Control**: 1-800-222-1222 (US)

---

**Remember: This tool is designed to support, not replace, professional medical judgment. When in doubt, always consult with qualified healthcare professionals.**

*Stay healthy and use this tool responsibly! 💚*
