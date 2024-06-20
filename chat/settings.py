from dotenv import load_dotenv
import os

load_dotenv()

# App settings
ACTIVE_LLM = "openai"
KNOWLEDGE_SOURCES = ["confluence", "filesystem"]
VECTOR_STORAGE = "qdrant"
MAX_QUESTION_LENGTH = 250

#Confluence settings
RELEVANT_SPACES = ["SIC"]
CONFLUENCE_URL = "https://axudatic.udc.gal"
CONFLUENCE_USERNAME = os.getenv('CONFLUENCE_USERNAME')
CONFLUENCE_PASSWORD = os.getenv('CONFLUENCE_PASSWORD')
CONFLUENCE_PAGE_CHUNKSIZE = 30

#File settings
FILE_DATA_ROOT_FOLDER = "/code/files"
FILE_FOLDER_TREE_DEPTH = 5
FILE_EXTENSIONS = ["txt"]

#OpenAI settings
OPENAI_MODEL = "gpt-4"
OPENAI_EMBEDDING_MODEL = "text-embedding-ada-002"
OPENAI_MAX_TOKENS = 4000
OPENAI_API_KEY= os.getenv('OPENAI_API_KEY')


#QDrant settings
QDRANT_HOST = "qdrant"
QDRANT_PORT = 6333
QDRANT_DEFAULT_COLLECTION = "navi_collection"
QDRANT_RESULTS_LIMIT = 5