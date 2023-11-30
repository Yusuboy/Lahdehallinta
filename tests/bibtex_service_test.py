import unittest
from entities.source import Source
from services import source_service
from services.bibtex_service import Bibtex_Service
import os

class FakeSourceService:
    def __init__(self):
        self.books = [{
            "tag":"JK17",
            "title": "Jaanan Kirja",
            "author": "Jaana Virtanen",
            "publish_year": 1968,
            "publisher": "Otava"
        }]
        
    def get_books(self):
        return self.books
    
class TestSourceService(unittest.TestCase):
    def setUp(self):
        self.service_stub = FakeSourceService()
        self.bibtex_service = Bibtex_Service(self.service_stub)

    def test_bibtex_file_is_created_service(self):
        self.bibtex_service.create_bibtex_file("test")
        self.assertEqual(os.path.exists('bibtex_files/test.bib'), True)
        os.remove('bibtex_files/test.bib')