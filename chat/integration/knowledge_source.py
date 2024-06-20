import unicodedata
import os
import fnmatch

from abc import ABCMeta, abstractmethod
from typing import Dict, List
from atlassian import Confluence
from bs4 import BeautifulSoup
from html import unescape

from ..core.utils import KnowledgeData
from ..settings import CONFLUENCE_URL, CONFLUENCE_USERNAME, CONFLUENCE_PASSWORD, RELEVANT_SPACES, CONFLUENCE_PAGE_CHUNKSIZE, FILE_EXTENSIONS, FILE_FOLDER_TREE_DEPTH, FILE_DATA_ROOT_FOLDER


class KnowledgeSource(metaclass=ABCMeta):
    @abstractmethod
    def get_data_to_load(self) -> List[KnowledgeData]:
        pass


class ConfluenceSource(KnowledgeSource):
        
    def __init__(self):
        self.client = Confluence(
            url=CONFLUENCE_URL,
            username=CONFLUENCE_USERNAME,
            password=CONFLUENCE_PASSWORD
        )
    
    def get_data_to_load(self) -> List[KnowledgeData]:
        page_list = self.get_all_spaces_pages()
        data = [self.get_page_data(page) for page in page_list]
        return data

    def get_all_spaces_pages(self):
        spaces = self.client.get_all_spaces()["results"]
        page_list = []
        for s in spaces:
            if s["key"] in RELEVANT_SPACES or RELEVANT_SPACES == ["all"]:
                page_list.extend(self.get_all_pages_from_space(s["key"], CONFLUENCE_PAGE_CHUNKSIZE, "page"))
                page_list.extend(self.get_all_pages_from_space(s["key"], CONFLUENCE_PAGE_CHUNKSIZE, "blogpost"))
        return page_list
        
    def get_all_pages_from_space(self, space_key : str, chunk_size: int, type: str):
        start_index = 0
        all_pages = []
        pages = [None] * chunk_size
        while True:
            if len(pages) < chunk_size:
                break
            pages = self.client.get_space_content(space_key, depth="all", start=start_index, limit=chunk_size, content_type=type, expand="body.storage")["results"]
            all_pages.extend(pages)
            start_index += chunk_size
        return all_pages

    def get_page_data(self, page) -> KnowledgeData:
        soup = BeautifulSoup(unescape(page["body"]["storage"]["value"]), 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()
        for a in soup.find_all('a'):
            a.string = a.get_text() + ' '
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        text = unicodedata.normalize("NFKD", text)
        metadata = self.build_metadata(page)
        #print(f"Metadata: {metadata}, Text: {text}")
        return KnowledgeData(text, metadata)

    def build_metadata(self, page) -> Dict:
        title = page.get("title")
        source = "Confluence"
        location = CONFLUENCE_URL + page["_links"]["webui"]
        return {"source": source, "location": location, "title": title}
 
class FileSource(KnowledgeSource):
    def get_data_to_load(self) -> List[KnowledgeData]:
        data_to_load = []
        for extension in FILE_EXTENSIONS:
            files = self.list_files_with_extension(FILE_DATA_ROOT_FOLDER, extension, FILE_FOLDER_TREE_DEPTH)
            for file in files:
                text = self.get_file_as_text(file)
                metadata = self.build_metadata(file)
                data_to_load.append(KnowledgeData(text, metadata))
        return data_to_load


    def get_file_as_text(self, file_path: str) -> str:
        clean_file_text = ""
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.strip():
                    clean_file_text += line
        return clean_file_text

    def list_files_with_extension(self, directory: str, extension: str, depth: int) -> List[str]:
        files = []
        extension = "*." + extension
        for dirpath, dirnames, filenames in os.walk(directory):
            if dirpath.count(os.sep) - directory.count(os.sep) < depth:
                for filename in fnmatch.filter(filenames, extension):
                    files.append(os.path.join(dirpath, filename))
        return files

    def build_metadata(self, file_path) -> Dict:
        title = os.path.basename(file_path)
        source = "Filesystem"
        location = file_path
        return {"source": source, "location": location, "title": title}