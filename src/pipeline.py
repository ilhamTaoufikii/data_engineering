import json
import re
from utils import load_file_as_dataframe, clean_dataframe
from config import DRUGS_FILE, PUBMED_CSV_FILE, PUBMED_JSON_FILE, CLINICAL_TRIALS_FILE, OUTPUT_PATH

def run_pipeline():
    """Runs the data pipeline to process the CSV and JSON files and generate the output file."""
    drugs_df = load_file_as_dataframe(DRUGS_FILE)
    pubmed_df = load_file_as_dataframe(PUBMED_CSV_FILE)
    clinical_trials_df = load_file_as_dataframe(CLINICAL_TRIALS_FILE)

    # Clean data
    pubmed_df = clean_dataframe(pubmed_df)
    clinical_trials_df = clean_dataframe(clinical_trials_df)

    # Load PubMed JSON data
    with open(PUBMED_JSON_FILE, 'r') as json_file:
        pubmed_json = json.load(json_file)

    # Initialize dictionary to store medication mentions
    medication_mentions = {}
    
    # Iterate through each drug to find mentions in PubMed and Clinical Trials
    for _, row in drugs_df.iterrows():
        drug_name = row['drug']
        drug_mentions = []

        # Search for mentions in PubMed articles (CSV)
        for _, pubmed_row in pubmed_df.iterrows():
            if re.search(r'\b' + re.escape(drug_name) + r'\b', pubmed_row['title'], re.I):
                drug_mentions.append({
                    "journal": pubmed_row['journal'],
                    "publication_type": "PubMed",
                    "date": pubmed_row['date'],
                    "publication_id": pubmed_row['id'],
                    "title": pubmed_row['title']
                })

        # Search for mentions in PubMed articles (JSON)
        for pubmed_item in pubmed_json:
            if re.search(r'\b' + re.escape(drug_name) + r'\b', pubmed_item['title'], re.I):
                drug_mentions.append({
                    "journal": pubmed_item['journal'],
                    "publication_type": "PubMed (JSON)",
                    "date": pubmed_item['date'],
                    "publication_id": pubmed_item['id'],
                    "title": pubmed_item['title']
                })

        # Search for mentions in Clinical Trials
        for _, trial_row in clinical_trials_df.iterrows():
            if re.search(r'\b' + re.escape(drug_name) + r'\b', trial_row['scientific_title'], re.I):
                drug_mentions.append({
                    "journal": trial_row['journal'],
                    "publication_type": "Clinical Trial",
                    "date": trial_row['date'],
                    "publication_id": trial_row['id'],
                    "title": trial_row['scientific_title']
                })

        # Add drug mentions to the dictionary
        if drug_mentions:
            medication_mentions[drug_name] = {
                "drug_name": drug_name,
                "mentions": drug_mentions
            }

    # Save the results as a JSON file
    output_filename = OUTPUT_PATH + 'medication_mentions.json'
    with open(output_filename, 'w', encoding='utf-8') as json_output:
        json.dump(medication_mentions, json_output, indent=4, ensure_ascii=False)

    return output_filename

#BONUS
def extract_journal_with_most_unique_drugs(json_file):
    """Extracts the journal with the highest number of unique drugs mentioned."""
    with open(json_file, 'r', encoding='utf-8') as f:
        medication_mentions = json.load(f)

    journal_drug_count = {}
    
    for drug, details in medication_mentions.items():
        for mention in details['mentions']:
            journal = mention['journal']
            if journal not in journal_drug_count:
                journal_drug_count[journal] = set()
            journal_drug_count[journal].add(drug)

    # Find the journal with the most unique drugs
    max_journal = None
    max_count = 0
    for journal, drugs in journal_drug_count.items():
        unique_count = len(drugs)
        if unique_count > max_count:
            max_count = unique_count
            max_journal = journal

    # Prepare the result
    result = {
        "journal": max_journal,
        "unique_drug_count": max_count
    }

    # Save the results as a JSON file
    output_filename = OUTPUT_PATH + 'journal_with_most_unique_drugs.json'
    with open(output_filename, 'w', encoding='utf-8') as json_output:
        json.dump(result, json_output, indent=4, ensure_ascii=False)
    
    return result


def find_other_drugs_in_pubmed_not_in_clinical_trials(json_file, target_drug):
    """Finds other drugs mentioned in PubMed but not in Clinical Trials for a given target drug."""
    with open(json_file, 'r', encoding='utf-8') as f:
        medication_mentions = json.load(f)

    pubmed_drugs = set()
    clinical_trial_drugs = set()
    
    for drug, details in medication_mentions.items():
        for mention in details['mentions']:
            if mention['publication_type'] == "PubMed" or mention['publication_type'] == "PubMed (JSON)":
                pubmed_drugs.add(drug)
            elif mention['publication_type'] == "Clinical Trial":
                clinical_trial_drugs.add(drug)

    # Find drugs mentioned in PubMed but not in Clinical Trials
    other_drugs = pubmed_drugs - clinical_trial_drugs

    # Exclude the target drug from the results
    if target_drug in other_drugs:
        other_drugs.remove(target_drug)

    # Save the results as a JSON file
    output_filename = OUTPUT_PATH + 'other_drugs_in_pubmed.json'
    with open(output_filename, 'w', encoding='utf-8') as json_output:
        json.dump(list(other_drugs), json_output, indent=4, ensure_ascii=False)
    
    return output_filename
