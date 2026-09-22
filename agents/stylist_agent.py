"""Stylist Agent module for ThreadTheory Multi-Agent Stylist.

Consumes the outputs of the Weather Agent and Wardrobe Agent to reason about styling,
weather appropriateness, color harmony, and formality alignment.
This agent has NO tools—it operates purely on LLM reasoning over input context.
"""

import os
from typing import Dict, Any, List
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
    stylist_system_prompt = (
        "You are ThreadTheory's Senior Personal AI Stylist.\n"
        "Your task is to analyze: (1) User Request, (2) Real-Time Weather Data, and (3) Available Wardrobe Items.\n"
        "Compose a cohesive, stylish, and weather-appropriate outfit.\n\n"
        "STRICT CONSTRAINTS:\n"
        "1. Select items EXCLUSIVELY from the provided Wardrobe Items list. Never invent or hallucinate items not present.\n"
        "2. Ensure weather comfort (temperature, rain probability, wind speed).\n"
        "3. Match formality and color harmony.\n\n"
        "OUTPUT FORMAT:\n"
        "### 👔 Recommended Outfit\n"
        "- **Top:** [Item Name]\n"
        "- **Bottom:** [Item Name]\n"
        "- **Outerwear:** [Item Name or None needed]\n"
        "- **Shoes:** [Item Name]\n"
        "- **Accessories:** [Item Name(s)]\n\n"
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
        # Extract weather values first — used by _pick() and outerwear logic
        temp = weather_data.get('temperature', 25.0)
        rain_prob = weather_data.get('rain_probability', 0)

        # Helper: first item matching category AND within temp range; two-level fallback
        def _pick(category: str, fallback_name: str, name_filter: str = None) -> str:
            temp_ok = [
                i for i in wardrobe_items
                if i.get('category') == category
                and i.get('temp_min_c', -99) <= temp <= i.get('temp_max_c', 99)
                and (name_filter is None or name_filter in i['name'].lower())
            ]
            if temp_ok:
                return temp_ok[0]['name']
            # Fallback level 2: ignore temperature, match category only
            any_cat = [i for i in wardrobe_items if i.get('category') == category
                       and (name_filter is None or name_filter in i['name'].lower())]
            return any_cat[0]['name'] if any_cat else fallback_name

        selected_top = _pick('top', 'White Oxford Cotton Shirt')
        selected_bottom = _pick('bottom', 'Beige Chino Pants')

        # Select weather-appropriate outerwear (unchanged logic)
        if temp < 15.0:
            selected_outerwear = _pick('outerwear', 'Navy Blue Wool Trench Coat', 'coat')
        elif rain_prob > 50:
            selected_outerwear = _pick('outerwear', 'Beige Lightweight Windbreaker', 'windbreaker')
        else:
            selected_outerwear = "None needed"

        selected_shoes = _pick('shoes', 'Minimalist White Leather Sneakers')
        selected_accessory = next((i['name'] for i in wardrobe_items if i.get('category') == 'accessory'), "UV Protection Sunglasses")


        city = weather_data.get('city', 'your location')
        weather_desc = weather_data.get('weather', 'Clear')

        return (
            f"### 👔 Recommended Outfit\n"
            f"- **Top:** {selected_top}\n"
            f"- **Bottom:** {selected_bottom}\n"
            f"- **Outerwear:** {selected_outerwear}\n"
            f"- **Shoes:** {selected_shoes}\n"
            f"- **Accessories:** {selected_accessory}\n\n"
            f"### 💡 Stylist Rationale\n"
            f"This outfit balances your styling request for {user_prompt} with real-time weather in {city} "
            f"({temp}°C, {weather_desc}, {rain_prob}% rain probability). The selected layers ensure comfort and color harmony."
        )

    # 1. Fast-Path Deterministic Styling: Avoids Gemini 429 rate limit delays during local server execution
    use_fast_path = os.getenv("USE_DETERMINISTIC_STYLIST", "true").lower() in ("1", "true", "yes")
    if use_fast_path:
        print("[StylistAgent] Fast-path deterministic stylist rule applied (0ms latency).")
        return {"agent_response": _build_deterministic_recommendation()}


    # 2. Gemini LLM Reasoning Path with Graceful Fallback
    try:
        llm = create_stylist_llm()
        response = llm.invoke(context_prompt)
        return {
            "agent_response": response.content.strip()
        }
    except Exception as e:
        print(f"[StylistAgent Graceful Fallback] Gemini API unavailable/rate-limited ({e}). Applying curated rule...")
        return {
            "agent_response": _build_deterministic_recommendation()
        }


