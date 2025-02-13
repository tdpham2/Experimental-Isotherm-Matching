import os
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from MOFDataExtractor.tools.load_models import load_openai_model
from MOFDataExtractor.tools.data_extractor import convert_pdfs_to_text
from MOFDataExtractor.models.MOFCrystalData import MOFCollection
from MOFDataExtractor.graph.graph import construct_graph
from MOFDataExtractor.tools.save_json import save_to_json
class MOFDataExtractorAgent:
    def __init__(
            self,
            model_name="gpt-4o-mini",
            tools = None,
            prompt = None,
            api_key = None,
            temperature= 0            
    ):
        try:
            if model_name in ["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o"]:
                llm = load_openai_model(model_name=model_name, api_key=api_key, temperature=temperature)
                print(f"Loaded {model_name}")

        except Exception as e:
            print(e)
            print(f"Error with loading {model_name}")

        self.tools = [convert_pdfs_to_text]
        self.llm = llm

    def construct_graph(self):
        self.graph = construct_graph(tools=self.tools, llm=self.llm)
        return self.graph
    
    def run(self, query):
        graph = self.construct_graph()
        inputs = {"messages": [("user", query)]}
        for s in graph.stream(inputs, stream_mode="values"):
            message = s["messages"][-1]
            if isinstance(message, tuple):
                print(message)
            else:
                message.pretty_print()
    def visualize(self):
        graph = self.construct_graph()
        
        import nest_asyncio
        from IPython.display import Image, display
        from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles

        nest_asyncio.apply()  # Required for Jupyter Notebook to run async functions

        display(
            Image(
                graph.get_graph().draw_mermaid_png(
                    curve_style=CurveStyle.LINEAR,
                    node_colors=NodeStyles(first="#ffdfba", last="#baffc9", default="#fad7de"),
                    wrap_label_n_words=9,
                    output_file_path=None,
                    draw_method=MermaidDrawMethod.PYPPETEER,
                    background_color="white",
                    padding=6,
                )
            )
        )                



