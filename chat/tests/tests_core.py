from typing import List
import unittest
from unittest.mock import Mock, patch
from chat.core.core_service import CoreService
from chat.core.utils import KnowledgeData, MessageData
from chat.integration.factory import IntegrationFactory
from chat.integration.knowledge_source import KnowledgeSource
from chat.integration.vector_db_integration import VectorDBIntegration


class KnowledgeDataTests(unittest.TestCase):
    def setUp(self):
        self.text = "Test text"
        self.metadata = {"test_key": "test_value"}
        self.knowledge_data = KnowledgeData(self.text, self.metadata)

    def test_get_text(self):
        self.assertEqual(self.knowledge_data.get_text(), self.text)

    def test_set_text(self):
        new_text = "Updtaed text"
        self.knowledge_data.set_text(new_text)
        self.assertEqual(self.knowledge_data.get_text(), new_text)

    def test_get_metadata(self):
        self.assertEqual(self.knowledge_data.get_metadata(), self.metadata)

    def test_set_metadata(self):
        new_metadata = {"new_test_key": "new_test_value"}
        self.knowledge_data.set_metadata(new_metadata)
        self.assertEqual(self.knowledge_data.get_metadata(), new_metadata)

class TestMessageData(unittest.TestCase):
    def setUp(self):
        self.message_data = MessageData("Hello", "User")

    def test_get_text(self):
        self.assertEqual(self.message_data.get_text(), "Hello")

    def test_set_text(self):
        self.message_data.set_text("Hi")
        self.assertEqual(self.message_data.get_text(), "Hi")

    def test_get_origin(self):
        self.assertEqual(self.message_data.get_origin(), "User")

    def test_set_origin(self):
        self.message_data.set_origin("System")
        self.assertEqual(self.message_data.get_origin(), "System")


class TestCoreService(unittest.TestCase):
    def setUp(self):
        self.core_service = CoreService()

    @patch.object(IntegrationFactory, 'get_vector_db')
    def test_get_context_from_data(self, mock_get_vector_db):
        mock_vector_db = Mock(spec=VectorDBIntegration)
        mock_get_vector_db.return_value = mock_vector_db
        mock_vector_db.get_best_matches.return_value = []
        context = self.core_service.get_context_from_data("test")
        self.assertIsInstance(context, List)
        mock_get_vector_db.assert_called_once()
        mock_vector_db.get_best_matches.assert_called_once_with("test")

    @patch.object(IntegrationFactory, 'get_vector_db')
    @patch.object(IntegrationFactory, 'get_knowledge_sources')
    def test_load_vector_storage(self, mock_get_knowledge_sources, mock_get_vector_db):
        mock_vector_db = Mock(spec=VectorDBIntegration)
        mock_get_vector_db.return_value = mock_vector_db
        mock_knowledge_source = Mock(spec=KnowledgeSource)
        mock_get_knowledge_sources.return_value = [mock_knowledge_source]
        mock_knowledge_source.get_data_to_load.return_value = []
        self.core_service.load_vector_storage()
        mock_get_vector_db.assert_called_once()
        mock_get_knowledge_sources.assert_called_once()
        mock_vector_db.flush_data.assert_called_once()
        mock_vector_db.load_data.assert_called_once_with([])
