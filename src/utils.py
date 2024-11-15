import pandas as pd
import re
import chardet

def load_file_as_dataframe(file_path):
    """Loads a CSV file into a Pandas DataFrame."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        raise Exception(f"Error loading file '{file_path}': {str(e)}")

def clean_string(text):
    """Cleans strings, corrects encoding issues, and removes unwanted symbols."""
    if isinstance(text, str):
        # Remove escape sequences (e.g., \xc3\x28) that might appear
        text = re.sub(r'\\x[0-9a-fA-F]{2}', '', text)

        # Detect the encoding using chardet
        detected_encoding = chardet.detect(text.encode())['encoding']
        
        # Try to decode using the detected encoding, or assume UTF-8
        try:
            # Decode using the detected encoding, if possible
            text = text.encode(detected_encoding).decode('utf-8', errors='ignore')
        except UnicodeDecodeError:
            # If decoding fails, fall back to UTF-8 as a last resort
            text = text.encode('latin1').decode('utf-8', errors='ignore')
        
        # Remove specific unwanted symbols (parentheses)
        text = re.sub(r'[()]+', '', text)  # Removes all parentheses
        # Remove any malformed characters that aren't printable
        text = ''.join(c for c in text if c.isprintable())
        text = text.strip()  # Removes leading and trailing whitespace
    return text

def clean_dataframe(df):
    """Applies string cleaning to 'journal' and 'title' columns."""
    if 'journal' in df.columns:
        df['journal'] = df['journal'].apply(clean_string)
    if 'title' in df.columns:
        df['title'] = df['title'].apply(clean_string)
    return df
