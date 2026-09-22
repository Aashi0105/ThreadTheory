"""Weather Agent module for ThreadTheory Multi-Agent Stylist.

Wraps the Weather Tool into a LangChain tool and exposes a dedicated Weather Agent
powered by Gemini.
"""

import os
import re
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.weather import get_weather

# Explicitly load .env from project root directory
ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=ENV_PATH)


@tool
def fetch_weather_data(city: str) -> dict:
    """Fetches real-time weather information (temperature, weather condition, rain probability, wind speed) for a given city name.

    Args:
        city: The name of the city (e.g., 'Vadodara', 'London', 'Tokyo').
    """
    return get_weather(city)


def create_weather_llm() -> ChatGoogleGenerativeAI:
    """Initializes and returns the Gemini LLM bound with weather tools."""
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
        temperature=0.0,
        timeout=10
    )
    return llm.bind_tools([fetch_weather_data])


def _extract_city_fast(query: str) -> Optional[str]:
    """Extracts city name using regex pattern 'in <City>' or known city keywords."""
    match = re.search(r'\bin\s+([A-Za-z\s]+?)(?=\s+today|\s+for|\s+this|\s*\?|\s*\.|\s*$)', query, re.IGNORECASE)
    if match:
        city_candidate = match.group(1).strip()
        if len(city_candidate) > 2 and city_candidate.lower() not in ["a", "the", "my"]:
            return city_candidate
    
    for known in ["Vadodara", "London", "Tokyo", "Paris", "New York", "Mumbai", "Delhi"]:
        if known.lower() in query.lower():
            return known
    return None


def run_weather_agent(query: str) -> Dict[str, Any]:
    """Runs the Weather Agent to process a weather query, invoking the weather tool if needed.

    Args:
        query: User input query (e.g. "What is the weather like in Vadodara?").

    Returns:
        Dict containing:
            - agent_response: str (natural language summary)
            - weather_data: dict (structured weather metrics)
    """
    extracted_city = _extract_city_fast(query)

    # 1. Fast-Path Optimization if city is clearly extracted
    if extracted_city:
        try:
            print(f"[WeatherAgent FastPath] Fetching weather directly for parsed city: '{extracted_city}'")
            wdata = get_weather(extracted_city)
            summary = (
                f"Current weather in {wdata['city']} is {wdata['temperature']}°C with {wdata['weather'].lower()} "
                f"and {wdata['rain_probability']}% chance of rain."
            )
            return {
                "agent_response": summary,
                "weather_data": wdata
            }
        except Exception as err:
            print(f"[WeatherAgent FastPath Error] {err}, trying LLM route...")

    # 2. LLM Tool-Calling Path
    try:
        llm_with_tools = create_weather_llm()
        prompt = (
            f"You are a Weather Agent. Parse the city from the user request and call the 'fetch_weather_data' tool.\n"
            f"User Request: '{query}'"
        )
        ai_msg = llm_with_tools.invoke(prompt)

        weather_data = {}
        if hasattr(ai_msg, "tool_calls") and ai_msg.tool_calls:
            for tool_call in ai_msg.tool_calls:
                if tool_call["name"] == "fetch_weather_data":
                    city_arg = tool_call["args"].get("city", "")
                    print(f"[WeatherAgent] LLM triggered tool 'fetch_weather_data' with city='{city_arg}'")
                    weather_data = get_weather(city_arg)
                    break

        if not weather_data:
            target_city = extracted_city or "Vadodara"
            print(f"[WeatherAgent Fallback] Fetching weather for fallback city: '{target_city}'")
            weather_data = get_weather(target_city)

        summary_prompt = (
            f"Based on weather data: {weather_data}, provide a concise 2-sentence summary of weather for styling."
        )
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        final_response = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.2,
            timeout=10
        ).invoke(summary_prompt)

        return {
            "agent_response": final_response.content.strip(),
            "weather_data": weather_data
        }

    except Exception as e:
        print(f"[WeatherAgent Graceful Fallback] Gemini API unavailable/rate-limited: {e}")
        fallback_city = extracted_city or "Vadodara"
        try:
            wdata = get_weather(fallback_city)
            fallback_summary = (
                f"Weather for {wdata['city']}: {wdata['temperature']}°C, {wdata['weather']} "
                f"({wdata['rain_probability']}% rain probability)."
            )
            return {
                "agent_response": fallback_summary,
                "weather_data": wdata
            }
        except Exception:
            return {
                "agent_response": "Weather data currently unavailable.",
                "weather_data": {"city": fallback_city, "temperature": 25.0, "weather": "Clear", "rain_probability": 0, "wind_speed": 10.0}
            }

