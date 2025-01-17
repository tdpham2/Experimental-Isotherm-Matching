from MOFDataExtractor.agent.agent import MOFDataExtractorAgent

agent = MOFDataExtractorAgent()
graph = agent.construct_graph()

messages = graph.invoke({"messages": "Hello, how are you?"})
print(messages)


