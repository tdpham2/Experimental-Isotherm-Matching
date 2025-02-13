# MOFDataExtractor

**MOFDataExtractor** is a powerful LLM-based agent designed to extract crystal data of Metal-Organic Frameworks (MOFs) from scientific papers in PDF format. This project leverages advanced language models to efficiently process and extract structured material properties, aiding in the comparison of experimental and simulated adsorption isotherms.

## Features
- Extracts structured MOF data from scientific literature (PDFs).
- Facilitates comparison between experimental and simulated adsorption isotherms.
- Utilizes state-of-the-art language models for accurate information retrieval.

## Installation
### 1. Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/tdpham2/Experimental-Isotherm-Matching.git
cd Experimental-Isotherm-Matching
```

### 2. Set Up a Conda Environment
Create and activate a dedicated Conda environment:
```bash
conda create -n mof_data_extractor python=3.10
conda activate mof_data_extractor
```

### 3. Install Dependencies
The required dependencies are listed in `pyproject.toml`. Install them using:
```bash
pip install .
```

## Requirements
- **Python**: 3.10 or higher
- **Dependencies:**
  - `pydantic>=2.10.3`
  - `langgraph>=0.2.59`
  - `langchain-openai>=0.2.12,<0.3`
  - `pandas>=2.2`
  - `jupyter`

## Usage
After installation, you can use the **MOFDataExtractor** agent to extract crystal data from MOF-related PDFs. Ensure the system is configured to point to the target PDF file before execution.

## Contributing
Contributions are welcome! If you'd like to improve **MOFDataExtractor**, please follow these steps:
1. Fork this repository.
2. Make your changes.
3. Submit a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.
