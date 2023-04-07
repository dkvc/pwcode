import asyncio
import logging
import os

from fastapi import FastAPI, Response
from json import load as jsonload
from pathlib import Path
from random import randint
from tempfile import gettempdir

from pwcode.api.Paper import Paper
from pwcode.utils.ConfigReader import ConfigReader
from pwcode.utils.WebReader import WebReader
from pwcode.utils.RSSGenerator import store_rss
from pwcode.utils.AtomGenerator import store_atom
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
        store_rss(latest()["papers"])
        store_atom(latest()["papers"])

        logger.info("Updates Check Done")

        sleep_time = randint(6, 12)
        logger.info("Next Update Check: %s hrs from now", sleep_time)
        await asyncio.sleep(sleep_time * 3600)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(background_check())
    logger.info("A task for background_check is created.")


@app.get("/latest", summary="Latest papers")
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


@app.get("/status", summary="Health check", status_code=200)
def status():
    endpoint_status = "Endpoint healthy, 200 OK"
    logger.info(f"{status}", filename)
    return endpoint_status


@app.get("/paper/{paper}", summary="Get details of paper")
def get_paper(paper: str):
    logger.info("GET: Paper %s", paper)
    return Paper(paper).to_json()


@app.get("/rss.xml", summary="RSS Feed for latest papers")
@app.get("/rss", summary="RSS Feed for latest papers")
@app.get("/.rss", summary="RSS Feed for latest papers")
async def rss():
    with open("rss.xml", "r") as file:
        xml_content = file.read()
    logger.info("RSS File is being read.")
    return Response(content=xml_content, media_type="application/rss+xml")


@app.get("/atom.xml", summary="Atom Feed for latest papers")
@app.get("/atom", summary="Atom Feed for latest papers")
@app.get("/.atom", summary="Atom Feed for latest papers")
async def atom():
    with open("atom.xml", "r") as file:
        xml_content = file.read()

    logger.info("Atom File is being read.")
    return Response(content=xml_content, media_type="application/atom+xml")
