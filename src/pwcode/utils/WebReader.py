import json
import logging
import os
import requests
import shutil
import sys

from bs4 import BeautifulSoup
from pathlib import Path
from tempfile import gettempdir
from typing import List

from api.Paper import Paper
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = RotatingFileHandler("app.log", maxBytes=10000, backupCount=5)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class WebReader:
    """Class that reads latest papers from pwcode"""

    __lock = False

    def __get_url(self, page: int):
        __url = f"https://paperswithcode.com/latest?page={page}"
        logger.info("URL selected: %s", __url)
        return __url

    def get_papers(self, pages: int):
        if pages > 5:
            pages = 5

        latest = []
        cache = self.ids(Path(os.path.join(gettempdir(), "pwcids.json")))

        for page in range(1, pages + 1):
            response = requests.get(self.__get_url(page))
            content = response.content
            logger.info("Content received for page %s", page)

            soup = BeautifulSoup(content, "html.parser")
            papers = soup.find_all("div", {"class": "col-lg-9 item-content"})

            for paper in papers:
                paper_id = paper.find("a")["href"].split("/")[-1]
                if paper_id in cache:
                    break
                latest.append(paper_id)

        logger.info("Number of latest papers: %s", len(latest))
        self.__store_latest(latest, cache)

        return latest

    def ids(self, path: Path):
        if not self.cache_exists(path):
            self.__create_empty_cache(path)

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = file.read().splitlines()
                logger.info("File %s is being read.", path)
                return data
        except PermissionError:
            print("Error: Permission denied. Please check temp directory permissions.")
            sys.exit(1)

    def cache_exists(self, path: Path):
        return path.exists() and path.is_file()

    def __create_empty_cache(self, path):
        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write("")
            logger.info("File %s doesn't exist. Empty file is being created.", path)
        except PermissionError:
            print("Error: Permission denied. Please check temp directory permissions.")
            sys.exit(1)

    def __store_latest(self, latest: List[str], original: List[str]):
        __path = Path(os.path.join(gettempdir(), "pwclatestids.json"))

        try:
            with open(__path, "w", encoding="utf-8") as file:
                file.writelines([id + "\n" for id in latest])
            logger.info("IDs written to pwclatestids.json")

            __path = Path(os.path.join(gettempdir(), "pwclatest.json"))
            __lock = True
            shutil.copy(__path, Path(os.path.join(gettempdir(), "pwclatest_old.json")))

            data = {"papers": []}
            for id in latest:
                data["papers"].append(Paper(id).to_json())

                with open(__path, "w", encoding="utf-8") as file:
                    json.dump(data, file, skipkeys=True, indent=4)
            logger.info("Latest Papers written to pwclatest.json")

            __lock = False

            __path = Path(os.path.join(gettempdir(), "pwcids.json"))

            with open(__path, "w", encoding="utf-8") as file:
                file.writelines([id + "\n" for id in original + latest])
            logger.info("Latest Papers written to pwcids.json")

        except PermissionError:
            print("Error: Permission denied. Please check temp directory permissions.")
            sys.exit(1)

    def get_lock(self):
        return self.__lock
