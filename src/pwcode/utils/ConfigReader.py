from pathlib import Path

import json
import requests


class ConfigReader:
    """Class that creates, stores and looks for changes in config file"""

    _path: Path
    papers: int

    def __init__(self):
        self._path = Path.expanduser(Path("~/.pwconfig"))
        self.papers = 0

    def __exists(self):
        _path = self._path
        if not (_path.exists() and _path.is_file):
            print("File doesn't exist.")
            return False

        try:
            with open(_path, encoding="utf-8") as file:
                json.load(file)
        except json.JSONDecodeError:
            print("File is not a valid JSON file.")
            return False

        return True

    def look_for_changes(self):
        if not self.__exists():
            self.__autocreate()

        with open(self._path, encoding="utf-8") as file:
            data = json.load(file)

        papers = requests.get("https://paperswithcode.com/api/v1/papers/").json()
        self.papers = papers["count"]
        if value := self.papers > data["papers"]:
            # TODO: Temporary Link
            read_web(pages=value // 10)
