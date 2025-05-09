# Text Anonymization Script

This Python script anonymizes German text by removing or replacing Personally Identifiable Information (PII). It uses the `spaCy` library for Natural Language Processing (NLP) to identify entities like names and locations, and custom regular expressions to find other PII like email addresses, phone numbers, etc.

## Prerequisites

- **Python > 3.10+**: If you don't have Python 3.10 or above installed, you can download it from [python.org](https://www.python.org/downloads/).
- **pip**: Python's package installer. It usually comes with Python. If not, see [pip installation guide](https://pip.pypa.io/en/stable/installation/).

## Setup and Usage

Follow these steps to set up and run the script:

**1. Clone or Download the Code**

If you have git installed, you can clone the repository.
git clone https://github.com/Jochen3000/python-podojo-tools

**2. Create a Virtual Environment (Recommended)**

A virtual environment helps keep project dependencies separate. Open your terminal or command prompt in the project's root directory (where this `README.md` file is located).

- On macOS and Linux:

  ```bash
  python3 -m venv .venv
  ```

This command creates a directory named `.venv` which will contain the virtual environment.

**3. Activate the Virtual Environment**

Before installing packages or running the script, you need to activate the environment:

- On macOS and Linux:

  ```bash
  source .venv/bin/activate
  ```

  You should see `(.venv)` at the beginning of your terminal prompt.

**4. Install Required Packages**

With the virtual environment active, install the necessary Python packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

This will install `spacy` and its dependencies.

**5. Download the spaCy Language Model**

The script uses a German language model from spaCy. The script will attempt to download it automatically if it's not found. However, you can also download it manually by running:

```bash
python -m spacy download de_core_news_lg
```

**6. Prepare Your Input File**

The script is currently configured to read from `data/gespraech_beispiel.txt` and write the anonymized output to `data/gespraech_beispiel_anonymized.txt`.

- Make sure you have a directory named `data` in the project root.
- Place your German text file (e.g., `gespraech_beispiel.txt`) inside the `data` directory.
- If your input file has a different name or path, you'll need to modify these lines in `src/anonymize_text.py`:

  ```python
  input_file_path = "data/your_file_name.txt"
  output_file_path = "data/your_file_name_anonymized.txt"
  ```

**7. Run the Anonymization Script**

Navigate to the project's root directory in your terminal (if you're not already there) and ensure your virtual environment is still active. Then run the script:

```bash
python src/anonymize_text.py
```

The script will:

- Print the first 200 characters of the original text.
- Print the full anonymized text.
- Save the anonymized text to the specified output file (e.g., `data/gespraech_beispiel_anonymized.txt`).

## How it Works

1.  **Load Text**: The script reads the content from the input file.
2.  **spaCy Entity Recognition**: It uses the `de_core_news_lg` spaCy model to process the text and identify named entities such as:
    - `PER`: Persons (e.g., "Erika Mustermann")
    - `LOC`: Locations (e.g., "Berlin")
    - `ORG`: Organizations (e.g., "Firma GmbH")
      These entities are replaced with placeholders like `[PER]`, `[LOC]`, `[ORG]`.
3.  **Regex for Other PII**: Custom regular expressions are used to find and replace other sensitive information that spaCy might not categorize as a standard entity or that needs more specific handling, such as:
    - Email addresses (`[EMAIL]`)
    - Phone numbers (`[PHONE]`)
    - Dates (`[DATE_EXPLICIT]`, `[DATE_NUMERIC]`)
    - Various ID numbers (`[ID_STEUER]`, `[KUNDENNUMMER]`, etc.)
