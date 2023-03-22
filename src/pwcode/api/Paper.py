import pendulum
import requests

from dataclasses import dataclass
from typing import List, Union
from pendulum import Date


@dataclass
class Paper:
    """Class for storing information about a paper."""

    id: str
    title: Union[str, None] = None
    published: Date = pendulum.now().date()
    authors: List[str] = list()
    abstract: Union[str, None] = None

    pwc_url: Union[str, None] = None
    git_url: Union[str, None] = None
    pdf_url: Union[str, None] = None
    framework: Union[str, None] = None

    def __post_init__(self):
        """If id is given, call the api and get information about the paper using id."""
        self.pwc_url = f"https://paperswithcode.com/paper/{id}"

        api_url = f"https://paperswithcode.com/api/v1/papers/{id}"
        paper = requests.get(api_url).json()
        paper_git = requests.get(api_url + "/repositories/").json()
        paper_git = paper_git["results"][0]
        paper_keys, paper_git_keys = paper.keys(), paper_git.keys()

        self.title = paper["title"] if "title" in paper_keys else None
        self.published = (
            pendulum.parse(paper["published"]) if "published" in paper_keys else None
        )

        self.authors = paper["authors"] if "authors" in paper_keys else None
        self.abstract = paper["abstract"] if "abstract" in paper_keys else None

        self.pdf_url = paper["url_pdf"] if "url_pdf" in paper_keys else None
        self.git_url = paper_git["url"] if "url" in paper_git_keys else None

        self.framework = (
            paper_git["framework"] if "framework" in paper_git_keys else None
        )
