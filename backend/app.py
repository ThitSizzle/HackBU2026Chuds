import os
import time
import shutil
import sys

# This tells Python to look in the project root so it can find the 'backend' folder
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import YOUR specific functions from your files
from backend.models.analyzer import analyzeImage
from backend.models.LLMBackend import get_fashion_advice

WATCH_DIR = "data/uploads"
OUT_DIR = "data/processed"

os.makedirs(WATCH_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

def run_ai_pipeline(file_path):
    filename = os.path.basename(file_path)
    print(f"\n [NEW IMAGE]: {filename}")
    print("-" * 50)

    print(" Analyzing body proportions and skin tone...")
    results = analyzeImage(file_path)

    if results.get("error"):
        print(f" ANALYZER ERROR: {results['error']}")
        shutil.move(file_path, os.path.join(OUT_DIR, filename))
        return

    print(f" Shape: {results.get('bodyShape')}")
    print(f" Ratio: {results.get('ratio')}")
    print(f" Proportion: {results.get('proportion')}")
    print(f" Skin RGB: {results.get('skin_rgb')}")

    print("\n Consulting the AI Stylist...")
    try:
        advice = get_fashion_advice(results)
        print("\n✨ [AI FASHION ADVICE]:")
        print(advice)
        print("-" * 50)
    except Exception as e:
        print(f" LLM ERROR: {str(e)}")

    dest_path = os.path.join(OUT_DIR, filename)
    if os.path.exists(dest_path):
        os.remove(dest_path)
        
    shutil.move(file_path, dest_path)
    print(f"📁 Analysis complete. File moved to: {OUT_DIR}\n")

if __name__ == "__main__":
    print(f"fAIshion")
    print(f" Drop images into: {os.path.abspath(WATCH_DIR)}")
    print("⌨ Press Ctrl+C to stop.")

    try:
        while True:
            files = [f for f in os.listdir(WATCH_DIR) 
                     if f.lower().endswith(('.png', '.jpg', '.jpeg')) and not f.startswith('.')]
            
            for f in files:
                full_path = os.path.join(WATCH_DIR, f)
                time.sleep(1.0)
                run_ai_pipeline(full_path)
            
            time.sleep(1) 
    except KeyboardInterrupt:
        print("\n App stopped. Thank you for watching our HackBU demo!")