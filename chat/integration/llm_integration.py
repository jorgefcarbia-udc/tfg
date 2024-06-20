from abc import ABCMeta, abstractmethod
from typing import List

from ..core.utils import KnowledgeData,MessageData

from ..settings import  OPENAI_API_KEY, OPENAI_EMBEDDING_MODEL, OPENAI_MODEL
from openai import OpenAI



class LLMIntegration(metaclass=ABCMeta):

    @abstractmethod
    def get_response(self, question: str, context: List[KnowledgeData], history: List[MessageData]) -> str:
        pass



class OpenAIIntegration(LLMIntegration):
    
    def __init__(self):
        self.client: OpenAI = OpenAI(api_key=OPENAI_API_KEY)

    def get_response(self, question: str, context: List[KnowledgeData], history: List[MessageData]) -> str:
        message_feed = (
            self.prepare_system_prompt()  # Call the method using self.prepare_system_prompt()
        + self.prepare_context_prompt(context)
        + self.prepare_history_prompt(history)
        + self.prepare_user_prompt(question)
        )

        chat_completion = self.client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=message_feed
        )

        return chat_completion.choices[0].message.content

    def prepare_system_prompt(self) -> List[dict]:
        return [{"role": "system", "content": "You are a helpful assistant, act friendly and be honest. Your role is to answer questions related to the UDC, Universidade da Coruña, its IT Services and any technical problem a user of those services may experience. Do not answer any questions outside of this scope and do not provide responses if you are not completely sure. If you need more information to answer the question, ask the user for it. Only take into account the context provided (including links), but make it as it was your own knowledge and never say it was the user who shared it. Provide links from the context if you need to, but keep in mind to never disclose that these links come from the user. Any links you provide, make it so that they are in HTMl syntax, using <a></a>. If you don't now the answer say 'I don't know'. If the user enters any personal or sensitive information, stop and don't answer their question, just point out that they must not enter sensitive information. Speak only in Galician (galego)"}]

    def prepare_history_prompt(self, previous_messages : List[MessageData])  -> List[dict]:
        messages_text = []
        for message in previous_messages:
            messages_text.append({ "role": self.origin_to_openai_role(message.get_origin()), "content": message.get_text() })
        return messages_text
    
    def origin_to_openai_role(self, origin: str) -> str:
        if origin == "GPT":
            return "assistant"
        else:
            return "user"
        
    def prepare_context_prompt(self, knowledge_context : List[KnowledgeData]) -> List[dict]:
        complete_context = " ".join(data.get_text() for data in knowledge_context) 
        return [{"role": "user", "content": f"Take this into account as context for the rest of the conversation: {complete_context}"}]

    def prepare_user_prompt(self, prompt : str) -> List[dict]:
        return [{"role": "user", "content": prompt}]