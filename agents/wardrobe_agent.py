"""Wardrobe Agent module for ThreadTheory Multi-Agent Stylist.

Wraps the Wardrobe Tool into a LangChain tool and exposes a dedicated Wardrobe Agent
powered by Gemini.
"""

import os
from typing import Dict, Any, Optional, List, Tuple
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.wardrobe import get_wardrobe_items

# Load .env file explicitly from root directory
ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=ENV_PATH)


@tool
def fetch_wardrobe_inventory(
    category: Optional[str] = None,
    formality: Optional[str] = None,
    max_temp_c: Optional[float] = None
) -> list:
    """Queries the user's wardrobe inventory database to retrieve available clothes.

    Args:
        category: Optional category filter ('top', 'bottom', 'outerwear', 'shoes', 'accessory').
        formality: Optional formality level ('casual', 'smart casual', 'formal').
        max_temp_c: Optional current weather temperature in °C to filter comfortable items.
    """
    return get_wardrobe_items(category=category, formality=formality, max_temp_c=max_temp_c)


def create_wardrobe_llm() -> ChatGoogleGenerativeAI:
    """Initializes Gemini LLM bound with wardrobe query tools."""
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        abs_env = os.path.abspath(ENV_PATH)
        raise ValueError(
            f"No Gemini API key found in '.env'.\n"
            f"  -> Looked in: '{abs_env}'\n"
            f"  -> Please ensure '.env' has either GOOGLE_API_KEY=AIzaSy... or GEMINI_API_KEY=AIzaSy..."
        )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.0
    )
    return llm.bind_tools([fetch_wardrobe_inventory])


def _try_fast_inventory_lookup(query: str, max_temp_c: Optional[float] = None) -> Optional[Tuple[List[Dict[str, Any]], str]]:
    """Fast-path deterministic query parser for simple wardrobe queries.

    BENEFIT OF THIS OPTIMIZATION:
    Directly answers standard inventory lookup requests (e.g. 'show tops', 'formal clothes',
    'what clothes do I own') by querying tools/wardrobe.py directly. This conserves Gemini
    API free-tier quota (5 RPM limit), eliminates network overhead, and prevents 429 errors.
    """
    q = query.lower().strip()

    # Match category filter
    matched_category = None
    if "top" in q or "shirt" in q or "tee" in q or "sweater" in q:
        matched_category = "top"
    elif "bottom" in q or "pant" in q or "jean" in q or "trousers" in q or "short" in q:
        matched_category = "bottom"
    elif "outerwear" in q or "jacket" in q or "coat" in q or "windbreaker" in q:
        matched_category = "outerwear"
    elif "shoe" in q or "boot" in q or "sneaker" in q or "oxford" in q:
        matched_category = "shoes"
    elif "accessory" in q or "scarf" in q or "sunglasses" in q:
        matched_category = "accessory"

    # Match formality filter
    matched_formality = None
    if "formal" in q:
        matched_formality = "formal"
    elif "smart casual" in q:
        matched_formality = "smart casual"
    elif "casual" in q and "smart" not in q:
        matched_formality = "casual"

    # General list query match
    is_general_query = any(phrase in q for phrase in [
        "what clothes do i have", "what clothes do i own", "show my wardrobe",
        "show all clothes", "list my clothes", "in my closet", "my closet"
    ])

    if matched_category or matched_formality or is_general_query:
        items = get_wardrobe_items(category=matched_category, formality=matched_formality, max_temp_c=max_temp_c)
        if not items and max_temp_c is not None:
            # Fallback: retry without temperature constraint if temp filter returned 0 items
            items = get_wardrobe_items(category=matched_category, formality=matched_formality)

        if not items:
            summary = f"No clothing items matching your filter were found in your closet."
        else:
            item_lines = [f"- {item['name']} ({item['color']}, {item['category']})" for item in items]
            summary = f"Here are the matching items in your closet:\n" + "\n".join(item_lines)
        return items, summary

    return None


def run_wardrobe_agent(query: str, weather_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Runs the Wardrobe Agent to process a user closet inquiry.

    Args:
        query: User prompt (e.g., "Show my formal clothing", "What tops do I have?").
        weather_data: Optional weather dict from Weather Agent (provides temperature for filtering).

    Returns:
        Dict containing:
            - agent_response: str (natural language summary of closet findings)
            - wardrobe_items: list of dicts (matching items from SQLite)
    """
    weather_data = weather_data or {}
    current_temp = weather_data.get("temperature")  # float or None
    if current_temp is not None:
        print(f"[WardrobeAgent] Received live weather: {current_temp}°C — filtering wardrobe by temperature range")
    # 1. Fast-Path Optimization: Check for simple deterministic queries first
    fast_result = _try_fast_inventory_lookup(query, max_temp_c=current_temp)
    if fast_result is not None:
        items, summary = fast_result
        temp_str = f" (temp filter: {current_temp}°C)" if current_temp is not None else ""
        print(f"[WardrobeAgent FastPath] Resolved query directly via tools/wardrobe.py ({len(items)} items found){temp_str}")
        return {
            "agent_response": summary,
            "wardrobe_items": items
        }

    # 2. LLM Reasoning Path for complex or non-standard queries
    try:
        llm_with_tools = create_wardrobe_llm()

        prompt = (
            f"You are a Wardrobe Agent. Inspect the user request and invoke the 'fetch_wardrobe_inventory' tool "
            f"with appropriate category, formality, or max_temp_c parameters if applicable.\n"
            f"User Request: '{query}'"
        )

        ai_msg = llm_with_tools.invoke(prompt)

        items: List[Dict[str, Any]] = []
        tool_executed = False

        if hasattr(ai_msg, "tool_calls") and ai_msg.tool_calls:
            for tool_call in ai_msg.tool_calls:
                if tool_call["name"] == "fetch_wardrobe_inventory":
                    args = tool_call.get("args", {})
                    print(f"[WardrobeAgent] LLM triggered tool 'fetch_wardrobe_inventory' with args={args}")
                    items = get_wardrobe_items(
                        category=args.get("category"),
                        formality=args.get("formality"),
                        max_temp_c=args.get("max_temp_c")
                    )
                    tool_executed = True
                    break

        if not tool_executed:
            if weather_data:
                print("[WardrobeAgent Fallback] No specific tool call executed; providing climate-appropriate wardrobe items.")
                items = get_wardrobe_items(max_temp_c=current_temp)
            else:
                print("[WardrobeAgent Fallback] No specific tool call executed for query.")
                items = []

        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not items:
            summary_prompt = (
                f"User asked: '{query}'. Database returned 0 matching items. "
                f"Provide an honest 1-sentence answer stating no such items exist in their closet."
            )
        else:
            summary_prompt = (
                f"User asked: '{query}'. Matching items: {items}.\n"
                f"Provide a clear bulleted list summarizing these clothing items."
            )

        final_response = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.2
        ).invoke(summary_prompt)

        resp_text = final_response.content
        if isinstance(resp_text, list):
            resp_text = "".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in resp_text)
        elif not isinstance(resp_text, str):
            resp_text = str(resp_text)

        return {
            "agent_response": resp_text.strip(),
            "wardrobe_items": items
        }

    except Exception as e:
        # Graceful Rate Limit (429) & Exception Handling
        print(f"[WardrobeAgent Graceful Fallback] Gemini API unavailable/rate-limited: {e}")
        # Fall back to direct database retrieval, still applying temperature filter
        items = get_wardrobe_items(max_temp_c=current_temp)
        if not items:
            fallback_msg = f"No matching items found in your wardrobe for query '{query}'."
        else:
            item_list = ", ".join([item['name'] for item in items[:5]])
            fallback_msg = (
                f"I checked your closet directly: You have {len(items)} total items available, "
                f"including {item_list}."
            )
        
        return {
            "agent_response": fallback_msg,
            "wardrobe_items": items
        }

