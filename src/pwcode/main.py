import asyncio
import logging
import os

from fastapi import FastAPI
from json import load as jsonload
from pathlib import Path
from random import randint
from tempfile import gettempdir

from api.Paper import Paper
from utils.ConfigReader import ConfigReader
from utils.WebReader import WebReader
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = RotatingFileHandler("app.log", maxBytes=10485760, backupCount=5)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

app = FastAPI()
config = ConfigReader()
reader = WebReader()


async def background_check():
    while True:
        config.look_for_changes()
        logger.info("Updates Check Done")

        sleep_time = randint(6, 12)
        logger.info("Next Update Check: %s hrs from now", sleep_time)
        await asyncio.sleep(sleep_time * 3600)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(background_check())
    logger.info("A task for background_check is created.")


@app.get("/latest")
def latest():
    if reader.get_lock():
        filename = "pwclatest_old.json"
    else:
        filename = "pwclatest.json"

    __path = Path(os.path.join(gettempdir(), filename))
    with open(__path, "r", encoding="utf-8") as file:
        data = jsonload(file)

    logger.info("JSON file %s loaded successfully.", filename)
    return data


@app.get("/paper/{paper}")
def get_paper(paper: str):
    logger.info("GET: Paper %s", paper)
    return Paper(paper).to_json()
