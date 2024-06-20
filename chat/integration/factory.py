from typing import List

from ..integration.vector_db_integration import VectorDBIntegration, QdrantIntegration
from ..integration.llm_integration import LLMIntegration, OpenAIIntegration
from ..integration.knowledge_source import ConfluenceSource, KnowledgeSource, FileSource

from ..settings import KNOWLEDGE_SOURCES, ACTIVE_LLM, VECTOR_STORAGE


class IntegrationFactory:
    KNOWLEDGE_SOURCE_MAP = {
        "confluence": ConfluenceSource,
        "filesystem": FileSource
    }

    LLM_INTEGRATION_MAP = {
        "openai": OpenAIIntegration
    }

    VECTOR_DB_MAP = {
        "qdrant": QdrantIntegration
    }

    @classmethod
    def get_knowledge_sources(cls) -> List[KnowledgeSource]:
        return [cls.KNOWLEDGE_SOURCE_MAP[source]() for source in KNOWLEDGE_SOURCES if source in cls.KNOWLEDGE_SOURCE_MAP]

    @classmethod
    def get_llm_integration(cls) -> LLMIntegration:
        return cls.LLM_INTEGRATION_MAP.get(ACTIVE_LLM, LLMIntegration)()

    @classmethod
    def get_vector_db(cls) -> VectorDBIntegration:
        return cls.VECTOR_DB_MAP.get(VECTOR_STORAGE, VectorDBIntegration)()