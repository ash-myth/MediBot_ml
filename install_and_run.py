"""
Automated Installation and Setup Script
One-click installation for the Symptom Checker Chatbot
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

def print_banner():
    """Display welcome banner"""
    print("=" * 60)
    print("    ADVANCED SYMPTOM CHECKER CHATBOT")
    print("    Automated Installation & Setup")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"🐍 Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Python 3.8 or higher is required!")
        print("   Please upgrade Python and try again.")
        input("Press Enter to exit...")
        sys.exit(1)
    else:
        print("✅ Python version is compatible")

def check_and_install_pip():
    """Ensure pip is available and updated"""
    print("\n📦 Checking pip installation...")
    try:
        import pip
        print("✅ pip is available")
        
        # Upgrade pip
        print("🔄 Upgrading pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("✅ pip upgraded successfully")
        
    except ImportError:
        print("❌ ERROR: pip is not installed!")
        print("   Please install pip and try again.")
        input("Press Enter to exit...")
        sys.exit(1)

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing required packages...")
    
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ ERROR: requirements.txt not found!")
        print("   Make sure you're running this script from the correct directory.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    try:
        # Install requirements
        cmd = [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)]
        subprocess.check_call(cmd)
        print("✅ All packages installed successfully")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: Failed to install packages: {e}")
        print("\n🔧 Troubleshooting steps:")
        print("1. Try running: python -m pip install --upgrade pip")
        print("2. Install packages individually:")
        print("   pip install customtkinter pandas matplotlib numpy")
        input("Press Enter to exit...")
        sys.exit(1)

def verify_installations():
    """Verify that all required packages are properly installed"""
    print("\n🔍 Verifying package installations...")
    
    required_packages = [
        ("customtkinter", "CustomTkinter GUI framework"),
        ("pandas", "Data analysis library"),
        ("matplotlib", "Plotting library"),
        ("numpy", "Numerical computing"),
        ("PIL", "Image processing (Pillow)"),
        ("fuzzywuzzy", "Fuzzy string matching")
    ]
    
    failed_packages = []
    
    for package, description in required_packages:
        try:
            if package == "PIL":
                import PIL
            else:
                importlib.import_module(package)
            print(f"✅ {package} - {description}")
        except ImportError:
            print(f"❌ {package} - {description}")
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n❌ Failed to import: {', '.join(failed_packages)}")
        print("🔧 Try installing manually:")
        for package in failed_packages:
            print(f"   pip install {package}")
        input("Press Enter to continue anyway...")
    else:
        print("\n✅ All packages verified successfully!")

def create_desktop_shortcut():
    """Create desktop shortcut (Windows only)"""
    if sys.platform == "win32":
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            shortcut_path = os.path.join(desktop, "Symptom Checker.lnk")
            target = os.path.abspath("main_gui.py")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = f'"{target}"'
            shortcut.WorkingDirectory = os.path.dirname(target)
            shortcut.IconLocation = sys.executable
            shortcut.save()
            
            print("✅ Desktop shortcut created")
        except Exception as e:
            print(f"⚠️  Could not create desktop shortcut: {e}")

def run_application():
    """Launch the application"""
    print("\n🚀 Launching Symptom Checker Chatbot...")
    
    main_script = Path("main_gui.py")
    if not main_script.exists():
        print("❌ ERROR: main_gui.py not found!")
        print("   Make sure all files are in the correct directory.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    try:
        # Launch the application
        subprocess.Popen([sys.executable, str(main_script)])
        print("✅ Application launched successfully!")
        print("\n🎉 Installation Complete!")
        print("\nThe Symptom Checker Chatbot should now be running.")
        print("If the application doesn't start, try running 'python main_gui.py' manually.")
        
    except Exception as e:
        print(f"❌ ERROR: Failed to launch application: {e}")
        print("\n🔧 Try running manually: python main_gui.py")

def show_post_install_info():
    """Show important information after installation"""
    print("\n" + "=" * 60)
    print("    INSTALLATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    
    print("\n📝 IMPORTANT INFORMATION:")
    print("• This is a medical information tool for educational purposes only")
    print("• Always consult healthcare professionals for medical advice")
    print("• In emergencies, call your local emergency number immediately")
    print("• Your data is stored locally and never shared")
    
    print("\n🎯 HOW TO USE:")
    print("1. Type your symptoms in the chat box")
    print("2. Use quick buttons for common symptoms")
    print("3. Answer follow-up questions for better assessment")
    print("4. Review results in the side panel")
    print("5. Export reports if needed")
    
    print("\n🔧 FUTURE ACCESS:")
    print("• Run 'python main_gui.py' from this directory")
    print("• Or use the desktop shortcut (Windows)")
    print("• Check README.md for detailed documentation")

def main():
    """Main installation process"""
    try:
        print_banner()
        
        # Step 1: Check Python version
        check_python_version()
        
        # Step 2: Check and update pip
        check_and_install_pip()
        
        # Step 3: Install requirements
        install_requirements()
        
        # Step 4: Verify installations
        verify_installations()
        
        # Step 5: Create desktop shortcut (Windows)
        create_desktop_shortcut()
        
        # Step 6: Show post-install information
        show_post_install_info()
        
        # Step 7: Launch application
        print("\n" + "=" * 60)
        launch = input("Would you like to launch the application now? (y/n): ").strip().lower()
        if launch in ['y', 'yes', '']:
            run_application()
        else:
            print("\n✅ Installation complete. Run 'python main_gui.py' when ready.")
        
        input("\nPress Enter to exit...")
        
    except KeyboardInterrupt:
        print("\n\n❌ Installation cancelled by user.")
        input("Press Enter to exit...")
        
    except Exception as e:
        print(f"\n❌ Unexpected error during installation: {e}")
        print("Please try running the installation steps manually.")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
