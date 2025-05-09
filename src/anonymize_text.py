import spacy
import re

# Load the German spaCy model
# Make sure you have the model downloaded: python -m spacy download de_core_news_lg
try:
    nlp = spacy.load("de_core_news_lg")
except OSError:
    print("Downloading de_core_news_lg model...")
    spacy.cli.download("de_core_news_lg")
    nlp = spacy.load("de_core_news_lg")

def load_text(file_path):
    """Loads text from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def anonymize_text(text):
    """
    Anonymizes text by removing PII using spaCy and custom regex.
    """
    doc = nlp(text)
    anonymized_text_parts = list(text) # Convert to list of chars for easier replacement

    # Anonymize entities detected by spaCy
    for ent in reversed(doc.ents): # Reverse to handle nested entities and avoid index issues
        if ent.label_ in ["PER", "LOC", "ORG"]:
            # Replace entity text with a placeholder
            placeholder = f"[{ent.label_}]"
            # Directly replace in the list of characters
            for i in range(ent.start_char, ent.end_char):
                anonymized_text_parts[i] = "" # Clear the original characters
            anonymized_text_parts[ent.start_char:ent.start_char] = list(placeholder) # Insert placeholder at start

    # Convert list back to string for further regex processing
    current_text = "".join(anonymized_text_parts)

    # Define custom regex patterns for PII not always caught by spaCy
    # or needing specific placeholders
    pii_patterns = {
        "EMAIL": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "PHONE": r"\b\d{2,4}\s\d{6,}\b", # Matches 030 1234567 or 089 9876543
        "IBAN": r"\b[A-Z]{2}\d{2}\s?(\d{4}\s?){4}\d{2}\b", # Simple IBAN-like
        "CREDIT_CARD": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
        "DATE_EXPLICIT": r"\b\d{1,2}\.\s(?:Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)\s\d{4}\b", # 15. August 1985
        "DATE_NUMERIC": r"\b\d{2}\.\d{2}\.\d{4}\b", # 15.08.1985
        "ID_STEUER": r"\b\d{4}\b", # For "letzten vier Ziffern Ihrer Steuer-Identifikationsnummer" - this is very generic, be careful
        "KUNDENNUMMER": r"\b[A-Za-z]+(?:_[A-Za-z0-9]+){2,}\b", # EMuster_1985_A2B
        "MITARBEITERNR": r"\b[A-Z]\d{4,}\b", # M4321
        "REFNUMMER": r"\b[A-Z]{6,}-\d{7,}\b" # CHGREF-0012345
    }

    for pii_type, pattern in pii_patterns.items():
        # Using a function for replacement to avoid issues with overlapping matches if re.sub is used directly on a modified string
        def replace_match(match):
            return f"[{pii_type}]"
        current_text = re.sub(pattern, replace_match, current_text)


    # Specific handling for street addresses which might be partially caught by LOC
    # Example: "Hauptstraße 123" where "Hauptstraße" might be LOC.
    # This is complex and might require more sophisticated context analysis or rule-based systems.
    # For now, we rely on LOC and the specific regex patterns.

    return current_text

if __name__ == "__main__":
    # Note: The user mentioned "example.txt", but the attached file is "data/gespraech_beispiel.txt"
    # Using the attached file path.
    input_file_path = "data/gespraech_beispiel.txt"
    output_file_path = "data/gespraech_beispiel_anonymized.txt"

    original_text = load_text(input_file_path)
    print(f"--- Original Text (first 200 chars): ---")
    print(original_text[:200] + "..." if len(original_text) > 200 else original_text)
    print("\n" + "="*50 + "\n")

    anonymized_version = anonymize_text(original_text)

    print(f"--- Anonymized Text: ---")
    print(anonymized_version)

    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(anonymized_version)
    print(f"\nAnonymized text saved to {output_file_path}")

    # Example of how spacy identifies entities:
    # print("\n--- SpaCy Entity Recognition Example: ---")
    # doc_example = nlp("Erika Mustermann wohnt in Berlin und arbeitet bei der Firma GmbH. Ihre Telefonnummer ist 030 123456.")
    # for ent in doc_example.ents:
    #     print(ent.text, ent.start_char, ent.end_char, ent.label_) 