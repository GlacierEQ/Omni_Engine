import unittest
from unittest.mock import patch, MagicMock
from skills.integrations.vlex.vlex_client import VlexClient

class TestVlexClient(unittest.TestCase):
    @patch('requests.get')
    def test_search_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"results": [{"id": "1", "title": "Test case"}]}
        
        client = VlexClient(api_key="test_key")
        results = client.search("test query")
        
        self.assertIn("results", results)
        self.assertEqual(len(results["results"]), 1)
        self.assertEqual(results["results"][0]["title"], "Test case")

    @patch('requests.get')
    def test_get_document_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"id": "1", "full_text": "Content"}
        
        client = VlexClient(api_key="test_key")
        doc = client.get_document("1")
        
        self.assertEqual(doc["id"], "1")
        self.assertEqual(doc["full_text"], "Content")

if __name__ == '__main__':
    unittest.main()
