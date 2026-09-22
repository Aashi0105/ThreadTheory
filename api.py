"""Python HTTP API Backend for ThreadTheory Multi-Agent Stylist.

Exposes a REST API endpoint 'POST /recommend' that invokes the LangGraph Supervisor graph
and returns structured JSON recommendations to the Node.js / Express website server.
"""

import os
import sys
import re
import json
from typing import List, Dict, Any
from http.server import HTTPServer, BaseHTTPRequestHandler

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

def _load_env_file():
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip("'\"")

_load_env_file()
sys.path.append(os.path.dirname(__file__))


from graph import app_graph, AgentState


def parse_outfit_from_text(text: str, wardrobe_items: List[dict] = None) -> dict:
    """Parses structured outfit recommendations and matches item names to wardrobe database objects with IDs."""
    if wardrobe_items is None:
        wardrobe_items = []

    def _find_item(cat: str, raw_name: str) -> dict:
        clean_name = re.sub(r'[\*_`]+', '', raw_name).strip()
        clean = clean_name.lower()
        if clean and clean not in ("none", "none needed", "none.", "n/a"):
            # 1. Search wardrobe_items (from state) for matching name
            for item in wardrobe_items:
                if item.get("category", "").lower() == cat.lower() or cat.lower() in item.get("category", "").lower():
                    if clean in item.get("name", "").lower() or item.get("name", "").lower() in clean:
                        return {"id": item.get("id"), "name": item.get("name")}

            # 2. Fallback: Search the full SQLite wardrobe database (wardrobe.db) directly
            try:
                from tools.wardrobe import get_wardrobe_items
                db_items = get_wardrobe_items(category=cat) or get_wardrobe_items()
                for item in db_items:
                    if clean in item.get("name", "").lower() or item.get("name", "").lower() in clean:
                        return {"id": item.get("id"), "name": item.get("name")}
            except Exception:
                pass

            # 3. Search by category fallback in wardrobe_items
            for item in wardrobe_items:
                if item.get("category", "").lower() == cat.lower():
                    return {"id": item.get("id"), "name": item.get("name")}

        return {"id": None, "name": clean_name if clean_name else raw_name.strip()}

    raw_parsed = {
        "top": "White Oxford Cotton Shirt",
        "bottom": "Beige Chino Pants",
        "outerwear": "None needed",
        "shoes": "Minimalist White Leather Sneakers",
        "accessories": "None"
    }

    lines = text.split("\n")
    for line in lines:
        l = line.strip().lower()
        cleaned_line = re.sub(r'[\*_`]+', '', line).strip()
        cl_lower = cleaned_line.lower()

        if "top:" in l or "top:" in cl_lower:
            val = line.split(":", 1)[-1] if ":" in line else cleaned_line.split(":", 1)[-1]
            raw_parsed["top"] = re.sub(r'[\*_`]+', '', val).strip()
        elif "bottom:" in l or "bottom:" in cl_lower:
            val = line.split(":", 1)[-1] if ":" in line else cleaned_line.split(":", 1)[-1]
            raw_parsed["bottom"] = re.sub(r'[\*_`]+', '', val).strip()
        elif "outerwear:" in l or "outerwear:" in cl_lower:
            val = line.split(":", 1)[-1] if ":" in line else cleaned_line.split(":", 1)[-1]
            raw_parsed["outerwear"] = re.sub(r'[\*_`]+', '', val).strip()
        elif "shoes:" in l or "shoes:" in cl_lower:
            val = line.split(":", 1)[-1] if ":" in line else cleaned_line.split(":", 1)[-1]
            raw_parsed["shoes"] = re.sub(r'[\*_`]+', '', val).strip()
        elif "accessories:" in l or "accessory:" in l or "accessories:" in cl_lower or "accessory:" in cl_lower:
            val = line.split(":", 1)[-1] if ":" in line else cleaned_line.split(":", 1)[-1]
            raw_parsed["accessories"] = re.sub(r'[\*_`]+', '', val).strip()

    cleaned_top = re.sub(r'[\*_`]+', '', raw_parsed["top"]).strip()
    cleaned_bottom = re.sub(r'[\*_`]+', '', raw_parsed["bottom"]).strip()
    cleaned_outerwear = re.sub(r'[\*_`]+', '', raw_parsed["outerwear"]).strip()
    cleaned_shoes = re.sub(r'[\*_`]+', '', raw_parsed["shoes"]).strip()
    cleaned_accessories = re.sub(r'[\*_`]+', '', raw_parsed["accessories"]).strip()

    return {
        "top": _find_item("top", cleaned_top),
        "bottom": _find_item("bottom", cleaned_bottom),
        "outerwear": _find_item("outerwear", cleaned_outerwear),
        "shoes": _find_item("shoes", cleaned_shoes),
        "accessories": cleaned_accessories
    }



class LangGraphAPIHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler exposing POST /recommend and POST /api/recommend."""

    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
        """Health check and info endpoint."""
        clean_path = self.path.split("?")[0]
        if clean_path in ["/", "/health", "/api/health", "/recommend", "/api/recommend", "/api/recommendations", "/api/inspiration/recommend"]:

            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {
                "status": "ok",
                "service": "ThreadTheory LangGraph Multi-Agent REST API",
                "usage": "Send an HTTP POST request to /recommend with payload {\"prompt\": \"your styling request\"}"
            }
            self.wfile.write(json.dumps(response, indent=2).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


    def do_POST(self):
        """Recommendation endpoint."""
        clean_path = self.path.split("?")[0]
        if clean_path in ["/recommend", "/api/recommend", "/api/recommendations", "/api/inspiration/recommend"]:

            try:
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length).decode("utf-8")
                payload = json.loads(body) if body else {}

                user_prompt = payload.get("prompt") or payload.get("occasion") or "Smart casual outfit for Vadodara"
                city = payload.get("city", "Vadodara")
                if city and city not in user_prompt:
                    user_prompt += f" in {city}"

                print(f"[LangGraph API] Received recommendation request: '{user_prompt}'")

                initial_state: AgentState = {
                    "user_prompt": user_prompt,
                    "next_agent": "",
                    "weather_data": {},
                    "wardrobe_items": [],
                    "execution_trace": [],
                    "final_response": ""
                }

                # Invoke LangGraph multi-agent supervisor graph
                final_state = app_graph.invoke(initial_state)

                witems = final_state.get("wardrobe_items", [])
                wdata = final_state.get("weather_data", {})
                raw_response = final_state.get("final_response", "")
                parsed_outfit = parse_outfit_from_text(raw_response, witems)

                response_payload = {
                    "success": True,
                    "top": parsed_outfit.get("top"),
                    "bottom": parsed_outfit.get("bottom"),
                    "outerwear": parsed_outfit.get("outerwear"),
                    "shoes": parsed_outfit.get("shoes"),
                    "weather": {
                        "city": wdata.get("city", "Vadodara"),
                        "temperature": wdata.get("temperature", 26.2),
                        "condition": wdata.get("weather", "Clear"),
                        "rain_probability": wdata.get("rain_probability", 0),
                        "wind_speed": wdata.get("wind_speed", 10.0)
                    },
                    "recommended_outfit": parsed_outfit,
                    "full_recommendation": raw_response,
                    "execution_trace": final_state.get("execution_trace", []),
                    "retrieved_wardrobe_count": len(witems)
                }


                self.send_response(200)
                self._set_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response_payload).encode("utf-8"))

            except Exception as e:
                print(f"[LangGraph API Error] {e}")
                self.send_response(500)
                self._set_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                error_payload = {"success": False, "error": str(e)}
                self.wfile.write(json.dumps(error_payload).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


def run_api_server(port: int = 5000):
    """Starts the HTTP API server."""
    server_address = ("", port)
    httpd = HTTPServer(server_address, LangGraphAPIHandler)
    print(f"🚀 ThreadTheory LangGraph API server running at http://localhost:{port}/recommend")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down LangGraph API server...")
        httpd.server_close()


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    run_api_server(port=port)
