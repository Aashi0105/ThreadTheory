import sys
import os
import json
import threading
import time
import requests
from http.server import HTTPServer
from dotenv import load_dotenv

# Ensure root project directory is in python path & load .env explicitly
ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=ENV_PATH)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api import LangGraphAPIHandler, parse_outfit_from_text


def test_parse_outfit_from_text_markdown_stripping():
    """Verifies that markdown artifacts (*, _, `) are stripped from all fields and wardrobe IDs matched from DB."""
    markdown_text = (
        "### 👔 Recommended Outfit\n"
        "- **Top:** Graphic Vintage Tee\n"
        "- **Bottom:** Dark Wash Slim Jeans\n"
        "- **Outerwear:** Beige Lightweight Windbreaker\n"
        "- **Shoes:** Minimalist White Leather Sneakers\n"
        "- **Accessories:** UV Protection Sunglasses\n\n"
        "### 💡 Stylist Rationale\n"
        "A stylish outfit for rainy weather."
    )
    result = parse_outfit_from_text(markdown_text)
    assert result["top"]["id"] == 7
    assert result["top"]["name"] == "Graphic Vintage Tee"
    assert result["bottom"]["id"] == 9
    assert result["bottom"]["name"] == "Dark Wash Slim Jeans"
    assert result["outerwear"]["id"] == 3
    assert result["outerwear"]["name"] == "Beige Lightweight Windbreaker"
    assert result["shoes"]["id"] == 14
    assert result["shoes"]["name"] == "Minimalist White Leather Sneakers"
    assert result["accessories"] == "UV Protection Sunglasses"

    # Also test varied markdown styling (bold, italic, backticks, messy colons)
    messy_text = (
        "### 👔 Recommended Outfit\n"
        "- **Top**: **Graphic Vintage Tee**\n"
        "- _Bottom:_ `Dark Wash Slim Jeans`\n"
        "- *Outerwear:* **Beige Lightweight Windbreaker**\n"
        "- **Shoes**: `Minimalist White Leather Sneakers`\n"
        "- **Accessories:** *UV Protection Sunglasses*"
    )
    messy_result = parse_outfit_from_text(messy_text)
    assert messy_result["top"]["id"] == 7
    assert messy_result["bottom"]["id"] == 9
    assert messy_result["outerwear"]["id"] == 3
    assert messy_result["shoes"]["id"] == 14
    assert messy_result["accessories"] == "UV Protection Sunglasses"
    print("  ✓ Markdown stripping and wardrobe DB matching unit test passed.")


def test_api_recommend_endpoint():
    """Starts local API server, sends test request, and shuts down server cleanly."""
    port = 5005
    httpd = HTTPServer(("", port), LangGraphAPIHandler)

    def serve_single():
        httpd.handle_request()

    server_thread = threading.Thread(target=serve_single)
    server_thread.start()
    time.sleep(0.5)

    print("==================================================")
    print("      ThreadTheory API - LangGraph REST Test       ")
    print("==================================================\n")

    url = f"http://localhost:{port}/recommend"
    payload = {
        "prompt": "What should I wear for a smart casual meeting in Vadodara today?",
        "city": "Vadodara"
    }

    print(f"[TEST] Sending POST request to '{url}'...")
    print("  Payload:", payload)

    response = requests.post(url, json=payload, timeout=30)


    server_thread.join(timeout=2)
    httpd.server_close()

    print("  ✓ HTTP Status Code:", response.status_code)
    
    data = response.json()
    print("  ✓ JSON Response Data Received:\n")
    print(json.dumps(data, indent=2))

    assert response.status_code == 200
    assert data.get("success") is True
    assert "weather" in data
    assert "recommended_outfit" in data
    assert "execution_trace" in data

    print("\n🎉 LANGGRAPH REST API TEST PASSED PERFECTLY!")


if __name__ == "__main__":
    test_parse_outfit_from_text_markdown_stripping()
    test_api_recommend_endpoint()

