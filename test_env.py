import os
import sqlite3
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def check_imports():
    """Verify all required V1 dependencies are installed correctly."""
    print("[1/4] Checking Python dependencies...")
    try:
        import langgraph
        import langchain_core
        import langchain_google_genai
        import streamlit
        print("  ✓ LangGraph version:", getattr(langgraph, "__version__", "Installed"))
        print("  ✓ LangChain Core version:", getattr(langchain_core, "__version__", "Installed"))
        print("  ✓ LangChain Google GenAI version:", getattr(langchain_google_genai, "__version__", "Installed"))
        print("  ✓ Streamlit version:", getattr(streamlit, "__version__", "Installed"))
        print("  -> Dependencies imports SUCCESSFUL!\n")
        return True
    except ImportError as e:
        print(f"  ✗ Import Error: {e}")
        print("  -> Please run: pip install -r requirements.txt\n")
        return False

def check_gemini_api():
    """Verify Gemini API Key configuration and lightweight API call."""
    print("[2/4] Checking Gemini API Configuration...")
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        print("  ✗ GOOGLE_API_KEY is missing or set to placeholder in .env file.")
        print("  -> Action: Add your real API key to the .env file.")
        return False
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)
        response = llm.invoke("Hello, reply with 'Gemini OK' if you receive this message.")
        print(f"  ✓ Gemini API Response: '{response.content.strip()}'")
        print("  -> Gemini API Connection SUCCESSFUL!\n")
        return True
    except Exception as e:
        print(f"  ✗ Gemini API Call Failed: {e}\n")
        return False

def check_open_meteo():
    """Verify Open-Meteo public REST API access."""
    print("[3/4] Checking Open-Meteo Weather API access...")
    try:
        # Test query for London coordinates (lat=51.5074, lon=-0.1278)
        url = "https://api.open-meteo.com/v1/forecast?latitude=51.5074&longitude=-0.1278&current_weather=true"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
        temp = data.get("current_weather", {}).get("temperature")
        print(f"  ✓ Open-Meteo REST API reached! Current London temp: {temp}°C")
        print("  -> Open-Meteo API Connection SUCCESSFUL!\n")
        return True
    except Exception as e:
        print(f"  ✗ Open-Meteo Call Failed: {e}\n")
        return False

def check_sqlite_db():
    """Verify SQLite database initialization and querying."""
    print("[4/4] Checking SQLite Wardrobe Database...")
    db_path = os.path.join(os.path.dirname(__file__), "wardrobe.db")
    if not os.path.exists(db_path):
        print(f"  ✗ Database file '{db_path}' not found.")
        print("  -> Action: Run 'python setup_db.py' first.")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM wardrobe")
        count = cursor.fetchone()[0]
        conn.close()
        print(f"  ✓ Wardrobe DB found and accessible! Total items in wardrobe: {count}")
        print("  -> SQLite Database Verification SUCCESSFUL!\n")
        return True
    except Exception as e:
        print(f"  ✗ SQLite Verification Failed: {e}\n")
        return False

if __name__ == "__main__":
    print("==================================================")
    print("  ThreadTheory Phase 1 - Environment & Tech Stack Verification")
    print("==================================================\n")
    
    step1 = check_imports()
    if not step1:
        print("⚠️ Please install dependencies before proceeding.")
        exit(1)
        
    step4 = check_sqlite_db()
    step3 = check_open_meteo()
    step2 = check_gemini_api()
    
    if step1 and step2 and step3 and step4:
        print("🎉 ALL PHASE 1 VERIFICATION CHECKS PASSED PERFECTLY!")
        print("We are ready to move to Phase 2 (Weather Tool).")
    else:
        print("❌ Phase 1 setup has incomplete items. Check error messages above.")
