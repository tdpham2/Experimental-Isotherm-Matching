from MOFDataExtractor.agent.agent import MOFDataExtractorAgent
import os, json

agent = MOFDataExtractorAgent()
graph = agent.construct_graph()
path_to_pdf = "/Users/tpham2/work/projects/Experimental_isotherm_project/paper_storage"

list_of_dois = os.listdir(path_to_pdf)
#doi_names = [doi for doi in list_of_dois if doi.startswith("10.1039")]
doi_names = ["10.1021ic0609249"]
path_to_isodb = "/Users/tpham2/work/projects/Experimental_isotherm_project/Experimental-Isotherm-Matching/nist-isodb/Library/"

for doi in doi_names:
    output_file = f"{doi}.json"
    if os.path.isfile(output_file):
        continue
    adsorbents = []
    isotherms = os.listdir(os.path.join(path_to_isodb, doi))
    isotherms = [f for f in isotherms if f.endswith(".json")]
    for iso in isotherms:
        isopath = os.path.join(path_to_isodb, doi, iso)
        print(isopath)
        with open(isopath, 'r') as f:
            iso_data = json.load(f)

        adsorbent = iso_data["adsorbent"]["name"]
        if adsorbent not in adsorbents:
            adsorbents.append(adsorbent)
    try:
        query = f"What are the crystallographic information of the materials in {path_to_pdf}/{doi}"
        inputs = {"messages": query, "question": query}
        for s in graph.stream(inputs, stream_mode="values"):
            message = s["messages"][-1]
            if isinstance(message, tuple):
                print(message)
            else:
                message.pretty_print()
                final_output = message.content

        with open(output_file, "w") as f:
            if isinstance(final_output, tuple):
                f.write(str(final_output))
            else:
                f.write(final_output.__str__())

        print(f"Final output saved to {output_file}")
    except Exception as e:
        print(e)
        with open("log.txt", "a") as f:
            f.write(f"{doi}\n")
