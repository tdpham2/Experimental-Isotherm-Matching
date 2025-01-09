from get_data_from_api import MOFDataExtractor
import os, json, sys

mof_data_extractor = MOFDataExtractor()
dois = [sys.argv[1]]
basepath = '/home/tdpham/Dropbox/Northwestern/work/Experimental_isotherm_project/OpenAI/steps/automated_steps/convert_pdf_to_txt/batch3'
isodb_path = '/home/tdpham/Dropbox/Northwestern/work/Experimental_isotherm_project/OpenAI/steps/1_match_by_DOIs/csd/'

for doi in dois:
    if os.path.isdir(doi):
        continue
    try:
        isotherms = os.listdir(os.path.join(isodb_path, doi))
        print(isotherms)
    except FileNotFoundError:
        print(f"Missing {os.path.join(isodb_path, doi)}")
        continue
    # Get adsorbent name
    isotherms = [i for i in isotherms if '.cif' not in i]
    adsorbents = []
    for iso in isotherms:
        isopath = os.path.join(isodb_path, doi, iso)
        with open(isopath, 'r') as f:
            iso_data = json.load(f)

        adsorbent = iso_data["adsorbent"]["name"]
        if adsorbent not in adsorbents:
            adsorbents.append(adsorbent)
        # Get text from pdf
        with open(os.path.join(basepath, doi, 'combined_text.txt'), 'r') as f:
            text = f.read()

        for ida, adsorbent in enumerate(adsorbents):
            task_prompt = f"Analyze the attached text, which contains information about metal-organic frameworks and answer the following questions:\n1. What is the crystal data of {adsorbent}?\n We are interested in the cell lengths (a, b and c) and cell angles (alpha, beta and gamma). This information is often mentioned in the crystallographic data section. If the text did not mention a certain parameter, infer it from the crystal system, or point group.\n2. What is the CCDC number of {adsorbent}? \n\n{text}\n\""
            cte = MOFDataExtractor()
            task_output = cte.run(task_prompt)

            with open(f"{adsorbent}.json", "w") as f:
                json.dump(task_output.model_dump(), f)