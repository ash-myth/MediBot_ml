# Medibot Chatbot 🤖💊

An intelligent, ML-powered symptom checker application with natural language processing, machine learning disease prediction, and a modern GUI interface built using CustomTkinter and scikit-learn.



## ✨ Features

### 🧠 **ML-Powered Symptom Analysis**
- **Machine Learning Disease Prediction**: RandomForest classifiers for accurate condition prediction
- **Natural Language Processing**: Understands complex symptom descriptions in plain English
- **Intelligent Symptom Extraction**: Automatically identifies symptoms from detailed narratives
- **Severity Assessment AI**: ML-based severity prediction with confidence scoring
- **Enhanced Pattern Recognition**: Advanced aliases and context-based symptom detection

### 💬 **Advanced Chat Interface**
- **Smart Conversation Flow**: AI determines when to use ML analysis vs. simple symptom matching
- **Context-Aware Responses**: Generates human-friendly, empathetic responses
- **Complex Description Support**: Handles detailed flu-like symptom narratives
- **Real-time Processing**: Live symptom analysis with AI feedback
- **Quick Action Buttons**: Instant access to common symptoms

### 🔬 **Medical Intelligence Engine**
- **Comprehensive Knowledge Base**: 500+ medical conditions with treatment recommendations
- **Probability Scoring**: ML-driven condition likelihood with confidence intervals
- **Treatment Recommendations**: AI-curated treatment and prevention advice
- **Medical Disclaimers**: Built-in safety warnings and professional guidance
- **Evidence-Based Matching**: Scientifically-backed symptom-condition correlations

### 📊 **Analytics & Insights**
- **Real-time Assessment**: Live updates as symptoms are detected
- **Severity Visualization**: Dynamic progress bars and color-coded indicators
- **Condition Rankings**: Top conditions with percentage probabilities
- **Export Functionality**: Detailed JSON reports for medical consultations
- **Conversation History**: Complete chat logs with timestamps

### 📱 **User-Friendly Features**
- Dark/Light theme support
- Export functionality for medical records
- Conversation history tracking
- Searchable symptom selector
- Settings customization

### 🔒 **Privacy & Safety**
- Local data processing (no cloud dependency)
- Secure conversation logging
- Clear medical disclaimers
- Emergency guidance for serious symptoms

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Windows, macOS, or Linux

### Installation

1. **Download the Project Files**
   - Download all Python files to a single directory:
     - `main_gui.py`
     - `symptom_database.py`
     - `ml_analyzer.py`

2. **Install Required Dependencies**
   ```bash
   pip install customtkinter scikit-learn joblib numpy matplotlib
   ```

3. **Run the Application**
   ```bash
   python main_gui.py
   ```

### Example Usage Scenarios

**Simple Symptoms:**
- "I have a headache"
- "Feeling tired and nauseous"

**Complex ML Analysis:**
- "I've been experiencing flu-like symptoms for two days including high fever, severe body aches, fatigue, and chills"
- "Woke up with intense headache, feel very exhausted, and have been coughing all night with sore throat"

## 📋 System Requirements

- **Operating System:** Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Python:** 3.8 - 3.11
- **RAM:** 4GB minimum, 8GB recommended
- **Storage:** 100MB for application and dependencies
- **Display:** 1024x768 minimum resolution

## 🎯 How to Use

### Getting Started
1. Launch the application
2. Describe your symptoms in the chat box
3. Use quick buttons for common symptoms
4. Answer follow-up questions for better assessment
5. Review results in the side panel
6. Export reports for your records

### Chat Commands & Tips
- Type naturally: "I have a headache and feel nauseous"
- Use severity descriptors: "severe pain", "mild discomfort"
- Mention duration: "for 2 days", "since yesterday"
- Be specific about location: "left side of head", "upper chest"

### Quick Actions
- **🌡️ Fever** - Log fever symptoms
- **😷 Cough** - Record cough details
- **🤕 Headache** - Track headache patterns
- **😵 Nausea** - Monitor nausea episodes

## 🏗️ Architecture

```
symptom-checker-chatbot/
├── main_gui.py              # Main GUI application with ML integration
├── symptom_database.py      # Medical knowledge base & logic engine
├── ml_analyzer.py           # ML-powered symptom analysis engine
└── README.md               # Comprehensive documentation
```

### Core Components

1. **GUI Layer (`main_gui.py`)**
   - **Modern Interface**: CustomTkinter-based responsive design
   - **Smart Chat System**: Context-aware conversation handling
   - **ML Integration**: Automatic detection of complex symptom descriptions
   - **Real-time Updates**: Live symptom tracking and assessment panels
   - **Export System**: JSON report generation with conversation history

2. **ML Analysis Engine (`ml_analyzer.py`)**
   - **RandomForest Classifiers**: Disease and severity prediction models
   - **Feature Engineering**: Advanced symptom pattern extraction
   - **NLP Processing**: Regex-based symptom detection with medical aliases
   - **Model Training**: Automated training on enhanced medical datasets
   - **Response Generation**: Human-friendly diagnosis summaries

3. **Medical Database (`symptom_database.py`)**
   - **Knowledge Base**: 500+ medical conditions with detailed information
   - **Symptom Mapping**: Comprehensive symptom-disease relationships
   - **Probability Engine**: Weighted scoring and condition matching
   - **Treatment Database**: Evidence-based recommendations and prevention advice
   - **Follow-up Logic**: Context-aware question generation

### ML Pipeline Flow

1. **Input Processing**: User describes symptoms in natural language
2. **Smart Routing**: System determines ML vs. standard analysis based on input complexity
3. **Feature Extraction**: NLP extracts symptoms, severity, and context from text
4. **ML Prediction**: RandomForest models predict diseases and severity levels
5. **Knowledge Integration**: Results combined with medical database for recommendations
6. **Response Generation**: Human-friendly summary with treatment advice and disclaimers

## 📊 Supported Symptoms

### Respiratory
- Cough (dry/productive)
- Shortness of breath
- Chest pain
- Sore throat

### Gastrointestinal
- Nausea
- Vomiting
- Diarrhea
- Abdominal pain

### Neurological
- Headache
- Dizziness
- Fatigue

### General
- Fever
- Joint pain
- Muscle pain
- Rash
- Itching

## 🔧 Configuration

### Theme Settings
- **Dark Mode:** Default modern dark theme
- **Light Mode:** Clean light interface
- **System:** Follows OS theme preference

### Export Options
- **JSON:** Machine-readable format for data analysis
- **Text:** Human-readable format for sharing
- **Charts:** PNG images of analysis visualizations

## 🛡️ Medical Disclaimer

⚠️ **IMPORTANT MEDICAL DISCLAIMER** ⚠️

This application is for **informational and educational purposes only** and is not intended as a substitute for professional medical advice, diagnosis, or treatment. 

### Key Points:
- Always seek advice from qualified healthcare professionals
- Never ignore professional medical advice based on this tool
- In case of emergency, call emergency services immediately
- This tool cannot provide definitive medical diagnoses
- Results are suggestions based on symptom patterns only

### Emergency Situations
**Seek immediate medical attention if experiencing:**
- Severe chest pain or pressure
- Difficulty breathing
- Signs of stroke
- Severe allergic reactions
- Loss of consciousness
- Severe trauma or injury

## 🐛 Troubleshooting

### Common Issues

#### Installation Problems
```bash
# Update pip first
python -m pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v

# Try installing individually
pip install customtkinter pandas matplotlib numpy
```

#### GUI Not Loading
- Ensure Python 3.8+ is installed
- Try running with: `python -m tkinter` to test tkinter
- On Linux, install: `sudo apt-get install python3-tk`

#### Charts Not Generating
- Verify matplotlib installation: `pip show matplotlib`
- Install additional backends: `pip install matplotlib[gui]`
- Check file permissions in application directory

#### Performance Issues
- Close other applications to free memory
- Reduce conversation history: Settings → Clear History
- Update graphics drivers
- Try light theme mode

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Submit a pull request with detailed description

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings for all functions
- Include unit tests for new features
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Support

### Getting Help
- 📖 Check the [User Guide](USER_GUIDE.md)
- 🐛 Report issues on GitHub
- 💡 Request features via GitHub Issues
- 📧 Contact: [your-email@example.com]

### Community
- ⭐ Star this repo if you find it helpful
- 🔗 Share with others who might benefit
- 🤝 Contribute improvements and fixes

## 🔄 Version History

### v1.0.0 (Current) - ML-Enhanced Release
- ✅ **ML-Powered Symptom Analysis**: RandomForest classifiers for disease and severity prediction
- ✅ **Natural Language Processing**: Advanced symptom extraction from complex descriptions
- ✅ **Intelligent Chat Interface**: Context-aware routing between ML and standard analysis
- ✅ **Enhanced Symptom Detection**: Comprehensive aliases and pattern matching
- ✅ **Medical Knowledge Base**: 500+ conditions with treatment recommendations
- ✅ **Human-Friendly Responses**: AI-generated empathetic and informative replies
- ✅ **Modern GUI**: CustomTkinter interface with real-time updates
- ✅ **Export Functionality**: JSON reports with conversation history
- ✅ **Comprehensive Documentation**: Updated with ML capabilities

### Key Accomplishments
- 🎆 **Successfully integrated machine learning** for complex symptom analysis
- 🎆 **Enhanced user experience** with intelligent conversation flow
- 🎆 **Improved accuracy** through ML-driven disease prediction
- 🎆 **Better symptom recognition** with natural language understanding


## 🙏 Acknowledgments

- **CustomTkinter** - Modern GUI framework for beautiful interfaces
- **scikit-learn** - Machine learning library for disease prediction
- **NumPy** - Numerical computing for data processing
- **Matplotlib** - Data visualization and charting
- **Joblib** - Model persistence and efficient computing
- **Python Community** - Open-source ecosystem and support
- **Medical Community** - Evidence-based symptom-disease relationships

---

**Made with ❤️ for better health awareness and education**

*Remember: This tool is designed to complement, not replace, professional medical care.*

