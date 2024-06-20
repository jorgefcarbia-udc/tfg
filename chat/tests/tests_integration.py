import unittest, os
from unittest.mock import patch, Mock
from typing import List
from chat.core.utils import KnowledgeData, MessageData
from chat.integration.knowledge_source import KnowledgeSource, FileSource
from chat.integration.llm_integration import LLMIntegration
from chat.integration.vector_db_integration import VectorDBIntegration
from chat.integration.factory import IntegrationFactory

from chat.settings import QDRANT_RESULTS_LIMIT, FILE_DATA_ROOT_FOLDER


class TestKnowledgeSource(unittest.TestCase):
    def setUp(self):
        self.knowledge_source = IntegrationFactory.get_knowledge_sources()

    def test_get_data(self):
        data = self.knowledge_source[0].get_data_to_load()
        self.assertIsInstance(data, List)
        self.assertTrue(len(data) > 0)
        self.assertIsInstance(data[0], KnowledgeData)
        
class TestFileKnowledgeSource(unittest.TestCase):
    def setUp(self):
        self.knowledge_sources = IntegrationFactory.get_knowledge_sources()
        for source in self.knowledge_sources:
            if isinstance(source, FileSource):
                self.file_knowledge_source = source
                break

    def test_clean_empty_lines(self):
        folder_path = FILE_DATA_ROOT_FOLDER + "/test_get_data_to_load"
        os.makedirs(folder_path, exist_ok=True)
        text = "This is a test\n\n\n\n"
        file_path = folder_path + "/test.txt"
        with open(file_path, 'w') as file:
            file.write(text)

        cleaned_text = self.file_knowledge_source.get_file_as_text(file_path)
        self.assertIsInstance(cleaned_text, str)
        self.assertEqual(cleaned_text, "This is a test\n")
        os.remove(file_path)
        os.removedirs(folder_path)


    def test_get_data_to_load(self):
        folder_path = FILE_DATA_ROOT_FOLDER + "/test_get_data_to_load"
        os.makedirs(folder_path, exist_ok=True)
        text = "This is a test\n\n\n\n"
        file_path = folder_path + "/test.txt"
        with open(file_path, 'w') as file:
            file.write(text)

        data = self.file_knowledge_source.get_data_to_load()

        for knowledge_data in data:
            if knowledge_data.get_text() == "This is a test\n":
                inserted_data = knowledge_data

        self.assertIsInstance(data, List)
        self.assertTrue(len(data) > 0)
        self.assertIsInstance(inserted_data, KnowledgeData)
        self.assertEqual(inserted_data.get_text(), "This is a test\n")
        self.assertEqual(inserted_data.get_metadata(), {"source": "Filesystem", "location": folder_path + "/test.txt", "title": "test.txt"})
        
        os.remove(file_path)
        os.removedirs(folder_path)


class TestLLMIntegration(unittest.TestCase):
    def setUp(self):
        self.llm_integration = IntegrationFactory.get_llm_integration()

    def test_get_response(self):
        question = "Test question: answer just YES and nothing else. Do you understand?"
        context = [KnowledgeData("Test", {"test_key": "test_value"})]
        history = [MessageData("YES", "user"), MessageData("NO", "assistant")]
        response = self.llm_integration.get_response(question, context, history)
        self.assertIsInstance(response, str)
        self.assertEqual(response, "YES")


class TestVectorDBIntegration(unittest.TestCase):
    def setUp(self):
        self.vector_db_integration = IntegrationFactory.get_vector_db()


    def test_load_data(self):
        data = [KnowledgeData("Test0", {"test_key": "test_value"})]
        self.vector_db_integration.load_data(data)
        search = self.vector_db_integration.get_best_matches("Test0")
        self.assertIsInstance(search, List)
        self.assertEqual(len(search), 1)
        self.assertEqual(search[0].get_text(), "Test0")
        self.vector_db_integration.flush_data()

    def test_flush_data(self):
        data = [KnowledgeData("Test0", {"test_key": "test_value"})]
        self.vector_db_integration.load_data(data)
        self.vector_db_integration.flush_data()
        with self.assertRaises(Exception):
            self.vector_db_integration.get_best_matches("Test0")

    def test_get_best_matches(self):
        data = [KnowledgeData("Test #"+ str(i), {"test_key": "test_value"}) for i in range(10)]
        self.vector_db_integration.load_data(data)
        search = self.vector_db_integration.get_best_matches("0")
        self.assertIsInstance(search, List)
        self.assertEqual(len(search), QDRANT_RESULTS_LIMIT)
        self.vector_db_integration.flush_data()


if __name__ == '__main__':
    unittest.main()