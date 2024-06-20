from abc import abstractmethod, ABCMeta
from typing import List

from ..core.utils import KnowledgeData
from ..settings import QDRANT_HOST, QDRANT_PORT,QDRANT_DEFAULT_COLLECTION,QDRANT_RESULTS_LIMIT

from qdrant_client import QdrantClient


class VectorDBIntegration(metaclass=ABCMeta):
    @abstractmethod
    def load_data(self, data:List[KnowledgeData]) -> None:
        pass

    @abstractmethod
    def flush_data(self) -> None:
        pass    

    @abstractmethod
    def get_best_matches(self, question:str) -> List[KnowledgeData]:
        pass


class QdrantIntegration(VectorDBIntegration):
    def __init__(self):
        self.client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

    def load_data(self, knowledge_data : List[KnowledgeData]) -> None:
        texts = [data.get_text() for data in knowledge_data]
        metas = [data.get_metadata() for data in knowledge_data]
        self.client.add(
            collection_name=QDRANT_DEFAULT_COLLECTION,
            documents=texts,
            metadata=metas
        )

    def flush_data(self) -> None:
        self.client.delete_collection(collection_name=QDRANT_DEFAULT_COLLECTION)


    def get_best_matches(self, question:str) -> List[KnowledgeData]:
        search_result = self.client.query(
            collection_name=QDRANT_DEFAULT_COLLECTION,
            query_text=question,
            limit=QDRANT_RESULTS_LIMIT
        )
        best_matches = [KnowledgeData(result.document, result.metadata) for result in search_result]
        return best_matches
