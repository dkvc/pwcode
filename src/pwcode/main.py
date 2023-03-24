import asyncio
import os

from json import load as jsonload
from pathlib import Path
from random import randint
from tempfile import gettempdir
from utils.ConfigReader import ConfigReader
from api.Paper import Paper

from fastapi import FastAPI
from logging.handlers import RotatingFileHandler
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = FastAPI()
config = ConfigReader()
__path = Path(os.path.join(gettempdir(), "pwclatest.json"))


async def background_check():
    while True:
        config.look_for_changes()
        logger.info("Updated the file.")
        
        await asyncio.sleep(randint(12, 18) * 3600)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(background_check())
    logger.info("A task for background_check is created.")


@app.get("/latest")
def latest():
    with open(__path, "r", encoding="utf-8") as file:
        data = jsonload(file)
    
    logger.info("JSON file pwclatest.json loaded successfully.")
    return data


@app.get("/paper/{paper}")
def get_paper(paper: str):
    logger.info("GET: Paper %s", paper)
    return Paper(paper).to_json()
