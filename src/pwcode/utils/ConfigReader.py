import json
import logging
import os
import requests
import sys

from pathlib import Path

from utils.WebReader import WebReader
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = RotatingFileHandler("app.log", maxBytes=10485760, backupCount=5)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class ConfigReader:
    """Class that creates, stores and looks for changes in config file"""

    __path: Path
    papers: int

    def __init__(self):
        self.papers = 0

        if "XDG_CONFIG_HOME" in os.environ:
            self.__path = Path(os.environ["XDG_CONFIG_HOME"]).joinpath(".pwconfig")
        else:
            self.__path = Path.expanduser(Path("~/.config/.pwconfig"))

    def __exists(self):
        __path = self.__path
        if not (__path.exists() and __path.is_file):
            logger.info("File doesn't exist.")
            return False

        try:
            with open(__path, encoding="utf-8") as file:
                json.load(file)
        except json.JSONDecodeError:
            print("File is not a valid JSON file.")
            return False

        return True

    def __autocreate(self):
        logger.info("Config is being updated/created")
        config = {"papers": self.papers}
        try:
            with open(self.__path, "w", encoding="utf-8") as file:
                json.dump(config, file, skipkeys=True, indent=4)
            logger.info("Config dumped to %s", self.__path)

        except PermissionError:
            print(
                "Error: Permission Denied. Please check your home directory permissions."
            )
            sys.exit(1)

    def look_for_changes(self):
        if not self.__exists():
            self.__autocreate()

        with open(self.__path, encoding="utf-8") as file:
            data = json.load(file)
        logger.info("%s loaded successfully", self.__path)

        papers = requests.get("https://paperswithcode.com/api/v1/papers/").json()
        self.papers = papers["count"]
        reader = WebReader()

        if self.papers > data["papers"]:
            logger.info("Update for Latest Papers requested")
            pages = (self.papers - data["papers"]) // 10

            logger.info("%s pages requested", pages)
            reader.get_papers(pages=pages)
            self.__autocreate()
        else:
            logger.info("Nothing to update.")
