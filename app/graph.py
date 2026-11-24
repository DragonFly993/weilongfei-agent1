"""单工具 Agent 图：模型决定是否调用工具，工具执行后再回到模型。"""

from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from app.settings import load_config, resolve_api_key
from app.tools import sum_csv_column


def build_agent(config: dict | None = None):
    config = config or load_config()
    model_cfg = config["model"]
    tools = [sum_csv_column]
    model_kwargs = {
        "model": model_cfg["name"],
        "temperature": model_cfg["temperature"],
    }
    if model_cfg.get("base_url"):
        model_kwargs["base_url"] = model_cfg["base_url"]
    api_key = resolve_api_key(config)
    if api_key:
        model_kwargs["api_key"] = api_key
    model = ChatOpenAI(**model_kwargs).bind_tools(tools)

    def call_model(state: MessagesState):
        return {"messages": [model.invoke(state["messages"])]}

    graph = StateGraph(MessagesState)
    graph.add_node("agent", call_model)
    graph.add_node("tools", ToolNode(tools))
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")
    return graph.compile()
