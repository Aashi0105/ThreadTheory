"""LangGraph Multi-Agent Orchestrator module for ThreadTheory Multi-Agent Stylist.

Defines the shared AgentState and constructs the LangGraph StateGraph with Supervisor routing:
Supervisor -> Weather Agent -> Supervisor -> Wardrobe Agent -> Supervisor -> Stylist Agent -> FINISH.
"""

from typing import TypedDict, List, Dict, Any, Literal
from langgraph.graph import StateGraph, START, END

from agents.weather_agent import run_weather_agent
from agents.wardrobe_agent import run_wardrobe_agent
from agents.stylist_agent import run_stylist_agent


class AgentState(TypedDict):
    """Shared state object passed between agents in the LangGraph graph."""
    user_prompt: str
    next_agent: str
    weather_data: Dict[str, Any]
    wardrobe_items: List[Dict[str, Any]]
    execution_trace: List[str]
    final_response: str


def supervisor_node(state: AgentState) -> Dict[str, Any]:
    """Supervisor Agent logic: inspects current state and determines the next node.
    
    Routing order:
    1. If weather_data is empty -> route to 'weather_agent'
    2. If wardrobe_items is empty -> route to 'wardrobe_agent'
    3. If final_response is empty -> route to 'stylist_agent'
    4. Otherwise -> route to 'FINISH'
    """
    trace = list(state.get("execution_trace", []))
    
    if not state.get("weather_data"):
        next_agent = "weather_agent"
        print("[Supervisor] Routing -> Weather Agent")
        trace.append("Supervisor ➔ Weather Agent")
    elif not state.get("wardrobe_items"):
        next_agent = "wardrobe_agent"
        print("[Supervisor] Routing -> Wardrobe Agent")
        trace.append("Supervisor ➔ Wardrobe Agent")
    elif not state.get("final_response"):
        next_agent = "stylist_agent"
        print("[Supervisor] Routing -> Stylist Agent")
        trace.append("Supervisor ➔ Stylist Agent")
    else:
        next_agent = "FINISH"
        print("[Supervisor] Routing -> FINISH")
        trace.append("Supervisor ➔ FINISH")

    return {
        "next_agent": next_agent,
        "execution_trace": trace
    }


def weather_agent_node(state: AgentState) -> Dict[str, Any]:
    """Weather Agent node execution."""
    print("\n--- Executing Weather Agent ---")
    res = run_weather_agent(state["user_prompt"])
    trace = list(state.get("execution_trace", []))
    trace.append("Weather Agent Executed")
    return {
        "weather_data": res.get("weather_data", {}),
        "execution_trace": trace
    }


def wardrobe_agent_node(state: AgentState) -> Dict[str, Any]:
    """Wardrobe Agent node execution."""
    print("\n--- Executing Wardrobe Agent ---")
    res = run_wardrobe_agent(state["user_prompt"], state.get("weather_data", {}))
    trace = list(state.get("execution_trace", []))
    trace.append("Wardrobe Agent Executed")
    return {
        "wardrobe_items": res.get("wardrobe_items", []),
        "execution_trace": trace
    }


def stylist_agent_node(state: AgentState) -> Dict[str, Any]:
    """Stylist Agent node execution."""
    print("\n--- Executing Stylist Agent ---")
    res = run_stylist_agent(
        user_prompt=state["user_prompt"],
        weather_data=state.get("weather_data", {}),
        wardrobe_items=state.get("wardrobe_items", [])
    )
    trace = list(state.get("execution_trace", []))
    trace.append("Stylist Agent Executed")
    return {
        "final_response": res.get("agent_response", ""),
        "execution_trace": trace
    }


def create_multi_agent_graph():
    """Builds and compiles the LangGraph StateGraph."""
    builder = StateGraph(AgentState)

    # Add nodes
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("weather_agent", weather_agent_node)
    builder.add_node("wardrobe_agent", wardrobe_agent_node)
    builder.add_node("stylist_agent", stylist_agent_node)

    # Define entry point
    builder.add_edge(START, "supervisor")

    # Conditional routing from supervisor based on state['next_agent']
    builder.add_conditional_edges(
        "supervisor",
        lambda state: state["next_agent"],
        {
            "weather_agent": "weather_agent",
            "wardrobe_agent": "wardrobe_agent",
            "stylist_agent": "stylist_agent",
            "FINISH": END
        }
    )

    # Direct edges back to supervisor after each agent runs
    builder.add_edge("weather_agent", "supervisor")
    builder.add_edge("wardrobe_agent", "supervisor")
    builder.add_edge("stylist_agent", "supervisor")

    return builder.compile()


# Export compiled graph instance
app_graph = create_multi_agent_graph()
