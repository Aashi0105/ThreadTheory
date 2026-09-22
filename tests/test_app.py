"""Standalone validation script for app.py compilation (Phase 8)."""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_app_imports():
    print("[TEST] Validating Streamlit app imports...")
    import app
    print("  ✓ app.py imported and compiled successfully!")
    print("  -> STREAMLIT APP TEST PASSED PERFECTLY!\n")

if __name__ == "__main__":
    test_app_imports()
