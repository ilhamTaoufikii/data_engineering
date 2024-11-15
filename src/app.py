from flask import Flask, jsonify
from pipeline import run_pipeline, extract_journal_with_most_unique_drugs, find_other_drugs_in_pubmed_not_in_clinical_trials
from config import OUTPUT_PATH
import json
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Medication Data Pipeline API. Use /run_pipeline to execute the pipeline."
    })

@app.route('/run_pipeline', methods=['GET'])
def run_pipeline_route():
    try:
        output_file = run_pipeline()
        return jsonify({
            "message": "Pipeline executed successfully",
            "output_file": output_file
        })
    except Exception as e:
        return jsonify({"message": f"An error occurred while executing the pipeline: {str(e)}"}), 500

@app.route('/journal_with_most_unique_drugs', methods=['GET'])
def journal_with_most_unique_drugs_route():
    try:
        # Call the function to get the journal with the most unique drugs
        result = extract_journal_with_most_unique_drugs(OUTPUT_PATH + 'medication_mentions.json')
        
        output_filename = os.path.join(OUTPUT_PATH, 'journal_with_most_unique_drugs.json')
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        
        # Save the result to the file
        with open(output_filename, 'w', encoding='utf-8') as json_output:
            json.dump(result, json_output, indent=4, ensure_ascii=False)
        
        # Return the result as JSON
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/other_drugs_in_pubmed/<target_drug>', methods=['GET'])
def other_drugs_in_pubmed_route(target_drug):
    try:
        # Running the function to get other drugs in PubMed but not in clinical trials
        output_file = find_other_drugs_in_pubmed_not_in_clinical_trials(OUTPUT_PATH + 'medication_mentions.json', target_drug)
        
        # Load the result from the generated JSON file
        with open(output_file, 'r', encoding='utf-8') as f:
            other_drugs = json.load(f)

        result = {
            "target_drug": target_drug,
            "other_drugs_in_pubmed_not_in_clinical_trials": other_drugs
        }

        # Return the result as JSON
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
