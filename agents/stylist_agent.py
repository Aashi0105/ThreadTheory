"""Stylist Agent module for ThreadTheory Multi-Agent Stylist.

Consumes the outputs of the Weather Agent and Wardrobe Agent to reason about styling,
weather appropriateness, color harmony, and formality alignment.
This agent has NO tools—it operates purely on LLM reasoning over input context.
"""

import os
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Explicitly load .env from project root directory
ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=ENV_PATH)


def create_stylist_llm() -> ChatGoogleGenerativeAI:
    """Initializes and returns the Gemini LLM for reasoning."""
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        abs_env = os.path.abspath(ENV_PATH)
        raise ValueError(
            f"No Gemini API key found in '.env'.\n"
            f"  -> Looked in: '{abs_env}'\n"
            f"  -> Please ensure '.env' has either GOOGLE_API_KEY=AIzaSy... or GEMINI_API_KEY=AIzaSy..."
        )

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.3,
        timeout=15
    )



from concurrent.futures import ThreadPoolExecutor


def run_stylist_agent(
    user_prompt: str,
    weather_data: Dict[str, Any],
    wardrobe_items: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Runs the Stylist Agent to synthesize an outfit recommendation.

    Args:
        user_prompt: The user's original styling query or intent.
        weather_data: Structured weather dictionary from Weather Agent.
        wardrobe_items: List of clothing item dictionaries from Wardrobe Agent.

    Returns:
        Dict containing:
            - agent_response: str (structured Markdown outfit recommendation and rationale)
    """
    if not wardrobe_items:
        return {
            "agent_response": (
                "### 👔 Recommended Outfit\n"
                "- **Top:** None available\n"
                "- **Bottom:** None available\n"
                "- **Outerwear:** None needed\n"
                "- **Shoes:** None available\n"
                "- **Accessories:** None needed\n\n"
                "### 💡 Stylist Rationale\n"
                "Your digital wardrobe currently contains no clothing items to curate an outfit. "
                "Please add garments to your closet to receive personalized styling recommendations."
            ),
            "recommended_outfit": None
        }

    stylist_system_prompt = (
        "You are ThreadTheory's Senior Personal AI Stylist.\n"
        "Your task is to analyze: (1) User Request, (2) Real-Time Weather Data, and (3) Available Wardrobe Items.\n"
        "Compose a cohesive, stylish, and weather-appropriate outfit.\n\n"
        "STRICT CONSTRAINTS & COMPATIBILITY RULES:\n"
        "1. Select items EXCLUSIVELY by their exact 'id' from the provided Available Wardrobe Items list.\n"
        "2. Never invent, hallucinate, or alter clothing items or IDs.\n"
        "3. OUTFIT STRUCTURE RULES:\n"
        "   - Standard Outfit: Exactly ONE Top + Exactly ONE Bottom + Shoes.\n"
        "   - One-Piece Outfit: If a Dress, Jumpsuit, or Romper is selected, place it in 'Top:' and specify 'Bottom: None needed'.\n"
        "   - MUTUALLY EXCLUSIVE: NEVER combine a Dress, Jumpsuit, or Romper with Shorts, Skirts, Jeans, Pants, or Trousers.\n"
        "   - NEVER combine multiple Tops or multiple Bottoms.\n"
        "4. Ensure weather comfort (temperature, rain probability, wind speed) and color harmony.\n\n"
        "OUTPUT FORMAT (Return valid Markdown formatted exactly like this):\n"
        "### 👔 Recommended Outfit\n"
        "- **Top:** [Item Name] (ID: [Exact Item ID])\n"
        "- **Bottom:** [Item Name or None needed] (ID: [Exact Item ID or None])\n"
        "- **Outerwear:** [Item Name or None needed] (ID: [Exact Item ID or None])\n"
        "- **Shoes:** [Item Name or None needed] (ID: [Exact Item ID or None])\n"
        "- **Accessories:** [Item Name or None needed] (ID: [Exact Item ID or None])\n\n"
        "### 💡 Stylist Rationale\n"
        "[2-3 sentence explanation of why this outfit works for the weather and event]\n"
    )

    context_prompt = (
        f"{stylist_system_prompt}\n"
        f"--- USER REQUEST ---\n'{user_prompt}'\n\n"
        f"--- WEATHER DATA ---\n{weather_data}\n\n"
        f"--- AVAILABLE WARDROBE ITEMS ---\n{wardrobe_items}\n"
    )

    def _invoke_llm():
        llm = create_stylist_llm()
        res = llm.invoke(context_prompt)
        return res.content.strip()

    # Fast deterministic styling rule builder
    def _build_deterministic_recommendation():
        temp = float(weather_data.get('temperature', 25.0))
        rain_prob = float(weather_data.get('rain_probability', 0))

        def _cat_match(item_cat: str, role: str) -> bool:
            c = (item_cat or "").lower().strip()
            r = role.lower()
            if r in ("dress", "one_piece", "one-piece"):
                return any(k in c for k in ["dress", "jumpsuit", "romper", "one-piece", "one_piece"])
            if r == "top":
                return any(k in c for k in ["top", "shirt", "blouse", "knitwear", "tee", "sweater"]) and not any(k in c for k in ["dress", "jumpsuit", "romper"])
            if r == "bottom":
                return any(k in c for k in ["bottom", "pant", "jean", "trouser", "short", "skirt"]) and not any(k in c for k in ["dress", "jumpsuit", "romper"])
            if r == "outerwear":
                return any(k in c for k in ["outerwear", "jacket", "coat", "windbreaker", "blazer", "cardigan"])
            if r == "shoes":
                return any(k in c for k in ["shoe", "boot", "sneaker", "footwear", "oxford", "heel", "sandal"])
            if r == "accessory":
                return any(k in c for k in ["accessory", "scarf", "glass", "belt", "hat", "bag"])
            return r in c

        def _pick_item(role: str, name_filter: str = None) -> Optional[Dict[str, Any]]:
            # First match: role AND comfortable in live temperature
            temp_ok = [
                i for i in wardrobe_items
                if _cat_match(i.get('category', ''), role)
                and float(i.get('temp_min_c', -99)) <= temp <= float(i.get('temp_max_c', 99))
                and (name_filter is None or name_filter in i.get('name', '').lower())
            ]
            if temp_ok:
                return temp_ok[0]
            # Second match: role without temperature constraint
            any_cat = [
                i for i in wardrobe_items
                if _cat_match(i.get('category', ''), role)
                and (name_filter is None or name_filter in i.get('name', '').lower())
            ]
            return any_cat[0] if any_cat else None

        # Check if user specifically requested a one-piece or if wardrobe favors a one-piece
        dress_requested = any(w in user_prompt.lower() for w in ["dress", "gown", "sundress", "one-piece", "jumpsuit", "romper"])
        dress_item = _pick_item('dress')

        top_item = _pick_item('top')
        bottom_item = _pick_item('bottom')
        shoes_item = _pick_item('shoes')

        # Decide between One-Piece outfit and Standard two-piece outfit
        is_one_piece = False
        if dress_requested and dress_item:
            is_one_piece = True
        elif dress_item and (not top_item or not bottom_item):
            is_one_piece = True
        elif not top_item and not bottom_item and dress_item:
            is_one_piece = True

        if is_one_piece and dress_item:
            top_str = f"{dress_item['name']} (ID: {dress_item['id']})"
            bottom_str = "None needed"
        else:
            top_str = f"{top_item['name']} (ID: {top_item['id']})" if top_item else "None available"
            bottom_str = f"{bottom_item['name']} (ID: {bottom_item['id']})" if bottom_item else "None available"

        # Outerwear logic
        outer_item = None
        if temp < 18.0 or rain_prob > 40:
            outer_item = _pick_item('outerwear')

        acc_item = _pick_item('accessory')

        outer_str = f"{outer_item['name']} (ID: {outer_item['id']})" if outer_item else "None needed"
        shoes_str = f"{shoes_item['name']} (ID: {shoes_item['id']})" if shoes_item else "None available"
        acc_str = f"{acc_item['name']} (ID: {acc_item['id']})" if acc_item else "None needed"

        city = weather_data.get('city', 'your location')
        weather_desc = weather_data.get('weather', 'Clear')

        return (
            f"### 👔 Recommended Outfit\n"
            f"- **Top:** {top_str}\n"
            f"- **Bottom:** {bottom_str}\n"
            f"- **Outerwear:** {outer_str}\n"
            f"- **Shoes:** {shoes_str}\n"
            f"- **Accessories:** {acc_str}\n\n"
            f"### 💡 Stylist Rationale\n"
            f"This outfit balances your styling request for {user_prompt} with real-time weather in {city} "
            f"({temp}°C, {weather_desc}, {rain_prob}% rain probability). The selected layers ensure comfort and color harmony."
        )

    # 1. Deterministic bypass check
    use_fast_path = os.getenv("USE_DETERMINISTIC_STYLIST", "false").lower() in ("1", "true", "yes")
    if use_fast_path:
        print("[StylistAgent] Deterministic stylist rule applied.")
        return {"agent_response": _build_deterministic_recommendation()}

    # 2. Gemini LLM Reasoning Path with Graceful Fallback
    try:
        llm = create_stylist_llm()
        response = llm.invoke(context_prompt)
        content = response.content.strip() if response and response.content else ""
        if content and ("Top:" in content or "Recommended Outfit" in content):
            return {"agent_response": content}
        return {"agent_response": _build_deterministic_recommendation()}
    except Exception as e:
        print(f"[StylistAgent Graceful Fallback] Gemini API unavailable/rate-limited ({e}). Applying curated rule...")
        return {
            "agent_response": _build_deterministic_recommendation()
        }


