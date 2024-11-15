import os
import unittest
from app import app
from config import OUTPUT_PATH

class FlaskAppTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Ensure the output directory exists for testing
        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH)

    def test_journal_with_most_unique_drugs(self):
        # Your test code here
        response = app.test_client().get('/journal_with_most_unique_drugs')
        self.assertEqual(response.status_code, 200)
        
        # Ensure the file exists after the request
        output_filename = os.path.join(OUTPUT_PATH, 'journal_with_most_unique_drugs.json')
        self.assertTrue(os.path.exists(output_filename))

    def test_other_drugs_in_pubmed(self):
        # Your test code here
        response = app.test_client().get('/other_drugs_in_pubmed/aspirin')
        self.assertEqual(response.status_code, 200)
        
        # Ensure the file exists after the request
        output_filename = os.path.join(OUTPUT_PATH, 'other_drugs_in_pubmed.json')
        self.assertTrue(os.path.exists(output_filename))

if __name__ == '__main__':
    unittest.main()
