from typing import Dict, Any

class KnowledgeData:
    def __init__(self, text: str, metadata: Dict[str, Any]):
        self.text = text
        self.metadata = metadata

    def get_text(self) -> str:
        return self.text

    def set_text(self, text: str) -> None:
        self.text = text

    def get_metadata(self) -> Dict[str, Any]:
        return self.metadata

    def set_metadata(self, metadata: Dict[str, Any]) -> None:
        self.metadata = metadata

    def __str__(self) -> str:
        return f"KnowledgeData(text={self.text}, metadata={self.metadata})"
    
    __repr__ = __str__

class MessageData:
    def __init__(self, text: str, origin: str):
        self.text = text
        self.origin = origin

    def get_text(self) -> str:
        return self.text
    
    def set_text(self, text: str) -> None:
        self.text = text

    def get_origin(self) -> str:
        return self.origin
    
    def set_origin(self, origin: str) -> None:
        self.origin = origin

    def __str__(self) -> str:
        return f"MessageData(text={self.text}, origin={self.origin})"