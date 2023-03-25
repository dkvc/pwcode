import logging
import requests

from dataclasses import dataclass, field
from typing import List, Union

from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = RotatingFileHandler("app.log", maxBytes=10485760, backupCount=5)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


@dataclass
class Paper:
    """Class for storing information about a paper."""

    id: str
    title: Union[str, None] = None
    published: Union[str, None] = None
    authors: List[str] = field(default_factory=lambda: [])
    abstract: Union[str, None] = None

    pwc_url: Union[str, None] = None
    git_url: Union[str, None] = None
    pdf_url: Union[str, None] = None
    framework: Union[str, None] = None

    def __post_init__(self):
        """If id is given, call the api and get information about the paper using id."""
        self.pwc_url = f"https://paperswithcode.com/paper/{self.id}"

        api_url = f"https://paperswithcode.com/api/v1/papers/{self.id}"
        paper = requests.get(api_url).json()
        paper_git = requests.get(api_url + "/repositories/").json()
        logger.info("URLs called successfully.")

        paper_git = paper_git["results"][0] if "results" in paper_git.keys() else {}
        paper_keys, paper_git_keys = paper.keys(), paper_git.keys()

        self.title = paper["title"] if "title" in paper_keys else None
        self.published = paper["published"] if "published" in paper_keys else None

        self.authors = paper["authors"] if "authors" in paper_keys else None
        self.abstract = paper["abstract"] if "abstract" in paper_keys else None

        self.pdf_url = paper["url_pdf"] if "url_pdf" in paper_keys else None
        self.git_url = paper_git["url"] if "url" in paper_git_keys else None

        self.framework = (
            paper_git["framework"] if "framework" in paper_git_keys else None
        )

        logger.info("All fields of Paper %s are initialized.", self.id)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "published": self.published,
            "authors": self.authors,
            "abstract": self.abstract,
            "pwc_url": self.pwc_url,
            "git_url": self.git_url,
            "pdf_url": self.pdf_url,
            "framework": self.framework,
        }
