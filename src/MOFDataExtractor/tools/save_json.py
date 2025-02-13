from langchain.tools import tool
import os
import json

@tool
def save_to_json(data, fname):
    """Save the json data to a file for later processing

    Args:
        json_data (dict): Information from LLM to save as JSON
        fname (str): File to store

    Raises:
    """
    try:
        with open(fname, "w'") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        raise Exception


    