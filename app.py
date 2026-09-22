"""Streamlit Web Interface module for ThreadTheory Multi-Agent Stylist (Phase 8).

Renders an interactive UI displaying:
1. User prompt input
2. Final Stylist Recommendation
3. Detailed Agent Execution Trace (Supervisor -> Weather -> Wardrobe -> Stylist -> Finished)
4. Context metrics (Weather & Wardrobe items retrieved)
"""

import sys
import os
import streamlit as st
from dotenv import load_dotenv

# Ensure root project directory is in python path & load .env explicitly
ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=ENV_PATH)
sys.path.append(os.path.dirname(__file__))

from graph import app_graph, AgentState

# Configure page metadata
st.set_page_config(
    page_title="ThreadTheory Multi-Agent Stylist",
    page_icon="👔",
    layout="wide"
)

st.title("👔 ThreadTheory Multi-Agent Stylist")
st.caption("Powered by LangGraph, Gemini & Open-Meteo")

st.markdown("""
---
This application orchestrates a team of specialized AI agents to generate personalized, weather-appropriate outfit recommendations from your closet database.
""")

# Sidebar: Architecture & Execution Trace explanation
with st.sidebar:
    st.header("⚙️ Multi-Agent Architecture")
    st.markdown("""
    **LangGraph Routing Workflow:**
    1. **Supervisor Agent** (Traffic Router)
    2. **Weather Agent** (Open-Meteo API)
    3. **Wardrobe Agent** (SQLite Inventory)
    4. **Stylist Agent** (Gemini Reasoning)
    """)
    st.divider()
    st.info("💡 Tip: Try queries specifying a city and event formality!")

# User input form
query = st.text_input(
    "Enter your outfit request:",
    value="What should I wear for a smart casual meeting in Vadodara today?",
    placeholder="e.g. What should I wear for a formal dinner in London?"
)

col_sample1, col_sample2 = st.columns(2)
if col_sample1.button("📋 Sample: Smart Casual in Vadodara"):
    query = "What should I wear for a smart casual meeting in Vadodara today?"
if col_sample2.button("📋 Sample: Formal Outfit in London"):
    query = "What should I wear for a formal evening event in London today?"

if st.button("✨ Style Me with LangGraph", type="primary"):
    if not query.strip():
        st.warning("Please enter a valid request.")
    else:
        initial_state: AgentState = {
            "user_prompt": query,
            "next_agent": "",
            "weather_data": {},
            "wardrobe_items": [],
            "execution_trace": [],
            "final_response": ""
        }

        with st.spinner("Orchestrating agents via LangGraph..."):
            final_state = app_graph.invoke(initial_state)

        st.subheader("🎉 Final Stylist Recommendation")
        st.markdown(final_state.get("final_response", "No response generated."))

        st.divider()

        # Context Metrics Section
        col_weather, col_wardrobe = st.columns(2)

        with col_weather:
            st.subheader("🌤️ Weather Context")
            wdata = final_state.get("weather_data", {})
            if wdata:
                st.metric("City", wdata.get("city", "Unknown"))
                st.metric("Temperature", f"{wdata.get('temperature', 0)} °C")
                st.metric("Condition", wdata.get("weather", "Unknown"))
                st.metric("Rain Probability", f"{wdata.get('rain_probability', 0)} %")
            else:
                st.write("No weather data retrieved.")

        with col_wardrobe:
            st.subheader("👔 Wardrobe Context")
            witems = final_state.get("wardrobe_items", [])
            st.metric("Items Selected", len(witems))
            if witems:
                with st.expander("View Retrieved Wardrobe Items"):
                    for item in witems:
                        st.write(f"• **{item['name']}** ({item['color']}, {item['category']}, {item['formality']})")

        st.divider()

        # Detailed Execution Trace Section
        st.subheader("📍 Agent Execution Trace")
        st.caption("LangGraph routing history showing Supervisor handoffs:")
        
        trace = final_state.get("execution_trace", [])
        if trace:
            for idx, step in enumerate(trace, 1):
                if "Supervisor" in step:
                    st.markdown(f"**Step {idx}:** `{step}`")
                elif "Executed" in step:
                    st.success(f"↳ **Step {idx}:** {step}")
                else:
                    st.write(f"**Step {idx}:** {step}")
