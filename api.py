"""Python HTTP API Backend for ThreadTheory Multi-Agent Stylist.

Exposes a REST API endpoint 'POST /recommend' that invokes the LangGraph Supervisor graph
and returns structured JSON recommendations to the Node.js / Express website server.
"""

import os
import sys
import re
import json
from typing import List, Dict, Any, Optional
from http.server import HTTPServer, ThreadingHTTPServer, BaseHTTPRequestHandler

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


def parse_outfit_from_text(text: str, wardrobe_items: List[dict] = None, user_email: Optional[str] = None) -> dict:
    """Parses structured outfit recommendations and matches item names to wardrobe database objects with IDs."""
    if wardrobe_items is None:
        wardrobe_items = []

    def _format_id(val: Any) -> Any:
        if val is None:
            return None
        s = str(val).strip()
        if s.isdigit():
            return int(s)
        return s

    def _format_item_dict(item: dict) -> dict:
        raw_id = item.get("id")
        img_url = item.get("processedImagePath") or item.get("processed_image_path") or item.get("img") or item.get("originalImagePath") or item.get("original_image_path") or ""
        return {
            "id": _format_id(raw_id),
            "name": item.get("name", ""),
            "category": item.get("category", ""),
            "color": item.get("color") or item.get("dominantColor") or "",
            "season": item.get("season", ""),
            "formality": item.get("formality") or item.get("occasion") or "",
            "img": img_url,
            "originalImagePath": item.get("originalImagePath") or item.get("original_image_path") or img_url,
            "processedImagePath": item.get("processedImagePath") or item.get("processed_image_path") or img_url
        }

    def _strip_markdown(s: str) -> str:
        if not s:
            return ""
        s = re.sub(r'[\*`#]+', '', s)
        s = re.sub(r'(?<!\w)_|_(?!\w)', '', s)
        return s.strip()


    def _find_item(cat: str, raw_name: str) -> Optional[dict]:
        if not raw_name:
            return None
        clean_name = _strip_markdown(raw_name)
        clean = clean_name.lower()
        if not clean or clean in ("none", "none needed", "none.", "n/a", "none available", "not specified"):
            return None

        # 1. Check for explicit (ID: ...) in raw_name
        id_match = re.search(r'\(id:\s*([^\)]+)\)', clean_name, re.IGNORECASE)
        if id_match:
            target_id = id_match.group(1).strip()
            # Check strictly in user's active wardrobe_items
            for item in wardrobe_items:
                if str(item.get("id")).strip() == target_id:
                    return _format_item_dict(item)
            # Check in SQLite wardrobe.db with strict user ownership
            try:
                from tools.wardrobe import get_wardrobe_item_by_id
                db_item = get_wardrobe_item_by_id(target_id, owner=user_email)
                if db_item:
                    return _format_item_dict(db_item)
            except Exception:
                pass
            return None

        # 2. Search wardrobe_items (from state) for matching name or ID
        if wardrobe_items:
            for item in wardrobe_items:
                item_name = item.get("name", "").lower()
                item_id = str(item.get("id", "")).lower()
                if item_id == clean or clean == item_name or (len(clean) >= 4 and clean in item_name):
                    return _format_item_dict(item)
            return None

        # 3. Search in SQLite wardrobe database directly if wardrobe_items was not provided
        try:
            from tools.wardrobe import get_wardrobe_items
            db_items = get_wardrobe_items(category=cat, owner=user_email) or get_wardrobe_items(owner=user_email)
            for item in db_items:
                item_name = item.get("name", "").lower()
                item_id = str(item.get("id", "")).lower()
                if item_id == clean or clean == item_name or (len(clean) >= 4 and clean in item_name):
                    return _format_item_dict(item)
        except Exception:
            pass

        return None

    raw_parsed = {
        "top": None,
        "bottom": None,
        "outerwear": None,
        "shoes": None,
        "accessories": None
    }

    lines = text.split("\n")
    for line in lines:
        l = line.strip().lower()
        cleaned_line = _strip_markdown(line)
        cl_lower = cleaned_line.lower()

        if "top:" in l or "top:" in cl_lower:
            val = line.split(":", 1)[-1] if ":" in line else cleaned_line.split(":", 1)[-1]
            raw_parsed["top"] = _strip_markdown(val)
        elif "bottom:" in l or "bottom:" in cl_lower:
            val = line.split(":", 1)[-1] if ":" in line else cleaned_line.split(":", 1)[-1]
            raw_parsed["bottom"] = _strip_markdown(val)
        elif "outerwear:" in l or "outerwear:" in cl_lower:
            val = line.split(":", 1)[-1] if ":" in line else cleaned_line.split(":", 1)[-1]
            raw_parsed["outerwear"] = _strip_markdown(val)
        elif "shoes:" in l or "shoes:" in cl_lower:
            val = line.split(":", 1)[-1] if ":" in line else cleaned_line.split(":", 1)[-1]
            raw_parsed["shoes"] = _strip_markdown(val)
        elif "accessories:" in l or "accessory:" in l or "accessories:" in cl_lower or "accessory:" in cl_lower:
            val = line.split(":", 1)[-1] if ":" in line else cleaned_line.split(":", 1)[-1]
            raw_parsed["accessories"] = _strip_markdown(val)

    cleaned_top = _strip_markdown(raw_parsed["top"]) if raw_parsed["top"] else ""
    cleaned_bottom = _strip_markdown(raw_parsed["bottom"]) if raw_parsed["bottom"] else ""
    cleaned_outerwear = _strip_markdown(raw_parsed["outerwear"]) if raw_parsed["outerwear"] else ""
    cleaned_shoes = _strip_markdown(raw_parsed["shoes"]) if raw_parsed["shoes"] else ""
    cleaned_accessories = _strip_markdown(raw_parsed["accessories"]) if raw_parsed["accessories"] else ""

    top_obj = _find_item("top", cleaned_top)
    bottom_obj = _find_item("bottom", cleaned_bottom)
    outerwear_obj = _find_item("outerwear", cleaned_outerwear)
    shoes_obj = _find_item("shoes", cleaned_shoes)

    # OUTFIT STRUCTURE / COMPATIBILITY MODEL
    # If the top object is a dress or one-piece (or clean text indicates dress/jumpsuit/romper),
    # then bottom MUST be None!
    is_one_piece = False
    if top_obj:
        top_cat = ((top_obj.get("category") or "") + " " + (top_obj.get("subcategory") or "")).lower()
        if any(k in top_cat for k in ["dress", "jumpsuit", "romper", "one-piece", "one_piece"]):
            is_one_piece = True
    if any(k in cleaned_top.lower() for k in ["dress", "jumpsuit", "romper", "one-piece"]):
        is_one_piece = True

    if is_one_piece:
        bottom_obj = None

    return {
        "top": top_obj,
        "bottom": bottom_obj,
        "outerwear": outerwear_obj,
        "shoes": shoes_obj,
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
                user_email = payload.get("email") or payload.get("user") or ""
                raw_wardrobe = payload.get("wardrobe") or []
                city = payload.get("city", "Vadodara")
                if city and city not in user_prompt:
                    user_prompt += f" in {city}"

                print(f"[LangGraph API] Received recommendation request: '{user_prompt}' (user: {user_email}, wardrobe_count: {len(raw_wardrobe)})")

                initial_state: AgentState = {
                    "user_prompt": user_prompt,
                    "user_email": user_email,
                    "raw_wardrobe": raw_wardrobe,
                    "next_agent": "",
                    "weather_data": None,
                    "wardrobe_items": None,
                    "execution_trace": [],
                    "final_response": None
                }

                # Invoke LangGraph multi-agent supervisor graph
                final_state = app_graph.invoke(initial_state)

                witems = final_state.get("wardrobe_items", []) or raw_wardrobe
                wdata = final_state.get("weather_data", {}) or {}
                raw_response = final_state.get("final_response", "") or ""
                parsed_outfit = parse_outfit_from_text(raw_response, witems, user_email=user_email)

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

            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
                print("[LangGraph API] Client connection closed or timed out before response was fully delivered.")
            except Exception as e:
                print(f"[LangGraph API Error] {e}")
                try:
                    self.send_response(500)
                    self._set_cors_headers()
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    error_payload = {"success": False, "error": str(e)}
                    self.wfile.write(json.dumps(error_payload).encode("utf-8"))
                except Exception:
                    pass
        else:
            self.send_response(404)
            self.end_headers()


def run_api_server(port: int = 5000):
    """Starts the HTTP API server."""
    server_address = ("", port)
    httpd = ThreadingHTTPServer(server_address, LangGraphAPIHandler)
    print(f"🚀 ThreadTheory LangGraph API server running at http://localhost:{port}/recommend")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down LangGraph API server...")
        httpd.server_close()


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    run_api_server(port=port)
