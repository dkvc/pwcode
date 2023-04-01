import pendulum
import logging

from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = RotatingFileHandler("app.log", maxBytes=10485760, backupCount=5)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def generate_rss(papers):
    time = pendulum.now().to_rss_string()
    rss = """\
<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">

<channel>
    <title>PapersWithCode Latest</title>
    <link>https://github.com/dkvc/pwcode</link>
    <description>Get Latest Papers from PapersWithCode</description>
    <language>en</language>
    <lastBuildDate>{}</lastBuildDate>
""".format(
        time
    )

    for paper in papers:
        description = """<![CDATA[<b>ID:</b> {}<br>
            <b>Repository URL:</b> <a href="{}">{}</a><br>
            <b>PDF URL:</b> <a href="{}">{}</a><br>
            <b>Abstract:</b> {}]]>
        """.format(
            paper["id"],
            paper["git_url"],
            paper["git_url"],
            paper["pdf_url"],
            paper["pdf_url"],
            paper["abstract"],
        )

        rss += """\
    <item>
        <title>{}</title>
        <link>{}</link>
        <author>{}</author>
        <description>{}</description>
        <pubDate>{}</pubDate>
    </item>""".format(
            paper["title"],
            paper["pwc_url"],
            ", ".join(paper["authors"]),
            description,
            paper["published"],
        )

    rss += "\n</channel>\n</rss>"

    logger.info("RSS Feed generated at %s", time)
    return rss


def store_rss(papers):
    with open("rss.xml", "w") as file:
        xml_content = generate_rss(papers)
        file.write(xml_content)
    
    logger.info("rss.xml is generated")
