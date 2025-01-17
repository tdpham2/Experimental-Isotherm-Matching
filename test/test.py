from MOFDataExtractor.agent.agent import MOFDataExtractorAgent

agent = MOFDataExtractorAgent()
graph = agent.construct_graph()
inputs = {"messages": "What are the information of the MOFs in paper_storage/10.1021ja904363b", "question": "What are the information of the MOFs in paper_storage/10.1021ja904363b"}
for s in graph.stream(inputs, stream_mode="values"):
    message = s["messages"][-1]
    if isinstance(message, tuple):
        print(message)
    else:
        message.pretty_print()

#output = graph.run()
#print("OUTPUT", output)


