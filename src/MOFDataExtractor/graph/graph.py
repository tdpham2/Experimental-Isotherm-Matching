from typing import Annotated, Literal
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import ToolMessage
import json
from langchain_openai import ChatOpenAI
from MOFDataExtractor.models.MOFCrystalData import MOFCollection, MOFData
from MOFDataExtractor.prompt.prompt import pdf_parser_prompt, data_extraction_prompt, router_prompt, regular_agent_prompt
from MOFDataExtractor.models.AgentResponse import RouterResponse
class State(TypedDict):
    messages: Annotated[list, add_messages]
    parsed_results: Annotated[list, add_messages]
    question: str
    router_response: Annotated[list, add_messages]

class BasicToolNode:
    """A node that runs the tools requested in the last AIMessage."""
    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs: State) -> State:
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")

        outputs = []
        parsed_results = []
        for tool_call in message.tool_calls:
            print("TOOL CALL", tool_call)
            try:
                tool_name = tool_call.get("name")
                if not tool_name or tool_name not in self.tools_by_name:
                    raise ValueError(f"Invalid tool name: {tool_name}")

                tool_result = self.tools_by_name[tool_name].invoke(
                    tool_call.get("args", {})
                )

                # Handle different types of tool results
                result_content = (
                    tool_result.dict() if hasattr(tool_result, "dict")
                    else tool_result if isinstance(tool_result, dict)
                    else str(tool_result)
                )
                parsed_results.append(result_content)

                outputs.append(
                    ToolMessage(
                        content=json.dumps(result_content),
                        name=tool_name,
                        tool_call_id=tool_call.get("id", ""),
                    )
                )
            except Exception as e:
                outputs.append(
                    ToolMessage(
                        content=json.dumps({"error": str(e)}),
                        name=tool_name if tool_name else "unknown_tool",
                        tool_call_id=tool_call.get("id", ""),
                    )
                )
        return {"messages": outputs, "parsed_results": parsed_results}

def route_tools(
    state: State,
):
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return "data_extraction"

def pdf_parser_agent(llm_with_tools: ChatOpenAI, state: State):
    """LLM node that processes messages and decides next actions."""
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response], "parsed_results": state["parsed_results"]}

def data_extraction_agent(llm, state: State):
    """LLM node that perform data extraction"""
    message = [
        {"role": "system", "content": data_extraction_prompt.format(text=state["parsed_results"][-1].content)},
        {"role": "user", "content": state["question"]}
    ]
    structure_llm = llm.with_structured_output(MOFCollection)
    response = structure_llm.invoke(message)
    return {"messages": [response.model_dump_json()]}

def router_agent(llm, state: State):
    """LLM node that handles routing question to appropriate agents"""
    message = [
        {"role": "system", "content": router_prompt},
        {"role": "user", "content": state["question"]}
    ]
    structure_llm = llm.with_structured_output(RouterResponse)
    response = structure_llm.invoke(message)
    return {"router_response": response.model_dump_json()}

def route_router(state: State) -> str:
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("router_response", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to route_router: {state}")
    # Parse the content into a dictionary
    try:
        content_dict = json.loads(ai_message.content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON content: {ai_message.content}") from e    
    # Access the 'next_agent' field
    next_agent = content_dict['next_agent']
    return next_agent

def regular_agent(llm, state: State):
    """LLM node that handles other inquiries"""
    message = [
        {"role": "system", "content": regular_agent_prompt},
        {"role": "user", "content": state["question"]}
    ]
    response = llm.invoke(message)
    return {"message": response}

def construct_graph(tools: list, llm: ChatOpenAI):
    tool_node = BasicToolNode(tools=tools)
    llm_with_tools = llm.bind_tools(tools)
    graph_builder = StateGraph(State)
    graph_builder.add_node("PDFParserAgent", lambda state: pdf_parser_agent(llm_with_tools, state))
    graph_builder.add_node("tools", tool_node)
    graph_builder.add_node("DataExtractionAgent", lambda state: data_extraction_agent(llm, state))
    graph_builder.add_node("RegularAgent", lambda state: regular_agent(llm, state))
    graph_builder.add_node("RouterAgent", lambda state: router_agent(llm, state))
    graph_builder.add_conditional_edges(
        "PDFParserAgent",
        route_tools,
        {
            "tools": "tools",   
            "data_extraction": "DataExtractionAgent"
        }
    )
    graph_builder.add_edge("tools", "PDFParserAgent")
    graph_builder.add_edge(START, "RouterAgent")
    graph_builder.add_conditional_edges(
        "RouterAgent",
        route_router,
        {
            "DataExtractionAgent": "PDFParserAgent",
            "RegularAgent": "RegularAgent"
        }
    )
    graph_builder.add_edge("RegularAgent", END)
    graph_builder.add_edge("DataExtractionAgent", END)

    graph = graph_builder.compile()

    return graph
