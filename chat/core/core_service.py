from .utils import KnowledgeData, MessageData
from ..integration.factory import IntegrationFactory
from ..integration.knowledge_source import KnowledgeSource
from ..integration.vector_db_integration import VectorDBIntegration
from ..integration.llm_integration import LLMIntegration
from ..settings import *
from typing import *

class CoreService:
    """
    This class provides core functionalities for the chat system.
    """

    @staticmethod
    def get_context_from_data(input : str) -> List[KnowledgeData]:
        """
        Retrieves the context from the given input data.

        Args:
            input (str): The input data.

        Returns:
            List[KnowledgeData]: The context retrieved from the input data.
        """
        try:
            vector_db : VectorDBIntegration = IntegrationFactory.get_vector_db()
            best_matches = vector_db.get_best_matches(input)
        except Exception as e:
            print(f"Error: {e}")
            best_matches = []
        return best_matches
    
    @staticmethod    
    def load_vector_storage() -> None:
        """
        Loads the vector storage with data from knowledge sources.

        Returns:
            None
        """
        knowledge_sources : List[KnowledgeSource] = IntegrationFactory.get_knowledge_sources()
        vector_db : VectorDBIntegration = IntegrationFactory.get_vector_db()

        vector_db.flush_data()
        for source in knowledge_sources:
            data = source.get_data_to_load()
            vector_db.load_data(data)
                
    @staticmethod
    def get_LLM_response(user_input: str, previous_messages: List[MessageData])-> Tuple[str, List[KnowledgeData]]:
        """
        Retrieves the response from the LLM integration based on the user input and previous messages.

        Args:
            user_input (str): The user input.
            previous_messages (List[MessageData]): The previous messages.

        Returns:
            Tuple[str, List[KnowledgeData]]: The response from the LLM integration and the context.
        """
        llm_integration : LLMIntegration = IntegrationFactory.get_llm_integration()
        context : List[KnowledgeData] =  CoreService.get_context_from_data(user_input)
        return llm_integration.get_response(user_input, context, previous_messages), context