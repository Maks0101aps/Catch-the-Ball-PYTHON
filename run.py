#!/usr/bin/env python3
import sys
import subprocess
import os
import platform

def is_venv_active():
    """Check if a virtual environment is active"""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def setup_venv():
    """Set up a virtual environment if not already active"""
    if is_venv_active():
        print("Virtual environment is already active.")
        return True
    
    try:
        # Check if venv directory exists
        if not os.path.exists("venv"):
            print("Creating virtual environment...")
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        
        # Activate venv and run the game inside it
        print("Activating virtual environment and installing dependencies...")
        
        if platform.system() == "Windows":
            activate_script = os.path.join("venv", "Scripts", "activate")
            python_exe = os.path.join("venv", "Scripts", "python.exe")
        else:
            activate_script = os.path.join("venv", "bin", "activate")
            python_exe = os.path.join("venv", "bin", "python")
        
        # Install requirements
        if platform.system() == "Windows":
            subprocess.run(f'"{python_exe}" -m pip install -r requirements.txt', shell=True, check=True)
        else:
            subprocess.run(f'. "{activate_script}" && pip install -r requirements.txt', shell=True, check=True)
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error setting up virtual environment: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    try:
        # Setup virtual environment if needed
        if not is_venv_active():
            success = setup_venv()
            if not success:
                print("Failed to set up virtual environment. Try running manually:")
                print("python -m venv venv")
                print("source venv/bin/activate  # On Linux/Mac")
                print("venv\\Scripts\\activate  # On Windows")
                print("pip install -r requirements.txt")
                sys.exit(1)
        
        # Run the game launcher
        if platform.system() == "Windows":
            python_exe = os.path.join("venv", "Scripts", "python.exe") if not is_venv_active() else sys.executable
            subprocess.run([python_exe, "launcher.py"])
        else:
            python_exe = os.path.join("venv", "bin", "python") if not is_venv_active() else sys.executable
            subprocess.run([python_exe, "launcher.py"])
            
    except KeyboardInterrupt:
        print("\nGame terminated by user.")
    except Exception as e:
        print(f"Error running the game: {e}") 