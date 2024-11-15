import os

# Environment variables for local file paths (instead of GCS)
DRUGS_FILE = os.getenv('DRUGS_FILE', 'data/drugs.csv')
PUBMED_CSV_FILE = os.getenv('PUBMED_CSV_FILE', 'data/pubmed.csv')
PUBMED_JSON_FILE = os.getenv('PUBMED_JSON_FILE', 'data/pubmed.json')
CLINICAL_TRIALS_FILE = os.getenv('CLINICAL_TRIALS_FILE', 'data/clinical_trials.csv')
OUTPUT_PATH = 'tmp/'
