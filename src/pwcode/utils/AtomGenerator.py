import pendulum
import logging

from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = RotatingFileHandler("app.log", maxBytes=10485760, backupCount=5)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def generate_atom(papers):
    time = pendulum.now().to_atom_string()
    atom = """\
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
    <title>PapersWithCode Latest</title>
    <link href="https://github.com/dkvc/pwcode" rel="alternate" />
    <link href="https://github.com/dkvc/pwcode/feed/atom" rel="self" />
    <id>https://github.com/dkvc/pwcode</id>
    <updated>{}</updated>
    <author>
        <name>PapersWithCode</name>
    </author>
""".format(
        time
    )

    for paper in papers:
        content = """<![CDATA[<b>ID:</b> {}<br>
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

        atom += """\
    <entry>
        <title>{}</title>
        <link href="{}" />
        <id>{}</id>
        <author>
            <name>{}</name>
        </author>
        <content type="html">{}</content>
        <published>{}</published>
    </entry>""".format(
            paper["title"],
            paper["pwc_url"],
            paper["pwc_url"],
            ", ".join(paper["authors"]),
            content,
            paper["published"],
        )

    atom += "\n</feed>"

    logger.info("Atom Feed generated at %s", time)
    return atom

def store_atom(papers):
    with open("atom.xml", "w") as file:
        xml_content = generate_atom(papers)
        file.write(xml_content)
    
    logger.info("atom.xml is generated")
