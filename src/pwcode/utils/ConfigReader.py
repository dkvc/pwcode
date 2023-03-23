from pathlib import Path

import json
import requests
import sys


class ConfigReader:
    """Class that creates, stores and looks for changes in config file"""

    __path: Path
    papers: int

    def __init__(self):
        self.__path = Path.expanduser(Path("~/.pwconfig"))
        self.papers = 0

    def __exists(self):
        __path = self.__path
        if not (__path.exists() and __path.is_file):
            print("File doesn't exist.")
            return False

        try:
            with open(__path, encoding="utf-8") as file:
                json.load(file)
        except json.JSONDecodeError:
            print("File is not a valid JSON file.")
            return False

        return True

    def __autocreate(self):
        config = {"papers": self.papers}
        try:
            with open(self._path, "w", encoding="utf-8") as file:
                json.dump(config, file, skipkeys=True, indent=4)
        except PermissionError:
            print(
                "Error: Permission Denied. Please check your home directory permissions."
            )
            sys.exit(1)

    async def look_for_changes(self):
        if not self.__exists():
            self.__autocreate()

        with open(self.__path, encoding="utf-8") as file:
            data = json.load(file)

        papers = await requests.get("https://paperswithcode.com/api/v1/papers/").json()
        self.papers = papers["count"]
        if value := self.papers > data["papers"]:
            # TODO: Temporary Link
            read_web(pages=value // 10)
