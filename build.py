#!/usr/bin/env python
"""
Vercel build script for Django
"""
import os
import subprocess
import sys

def run_command(command):
    """Run a command and return the result"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode == 0

def main():
    """Main build process"""
    print("Starting Django build process...")
    
    # Install requirements
    if not run_command("pip install -r requirements.txt"):
        print("Failed to install requirements")
        sys.exit(1)
    
    # Verify Django is installed
    try:
        import django
        print(f"Django {django.get_version()} installed successfully")
    except ImportError:
        print("Django not found after installation")
        sys.exit(1)
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FinanceFlow.settings')
    
    # Run Django setup
    django.setup()
    
    # Run migrations
    if not run_command("python manage.py makemigrations --noinput"):
        print("Failed to make migrations")
        sys.exit(1)
    
    if not run_command("python manage.py migrate --noinput"):
        print("Failed to run migrations")
        sys.exit(1)
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput --clear"):
        print("Failed to collect static files")
        sys.exit(1)
    
    print("Build completed successfully!")

if __name__ == "__main__":
    main()
