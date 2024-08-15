# PapersWithCode Latest (pwcode)

<h3>There will be no major updates for this project. Only security updates and bug fixes will be provided. The deployment will be continue running on Render until another solution is found.</h3>

## Get Latest Updates from PapersWithCode

This repository contains code for deployment of your own local server that retrieves latest PapersWithCode papers. You can also use web server hosted by us on [Render](https://pwcode.onrender.com/latest). The information can be retrieved in the form of [JSON](https://pwcode.onrender.com/latest), [RSS](https://pwcode.onrender.com/rss) or [Atom](https://pwcode.onrender.com/atom) feeds. Data is updated in all formats at same time.

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/dkvc/pwcode/main.svg)](https://results.pre-commit.ci/latest/github/dkvc/pwcode/main)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000)](https://github.com/psf/black)

## Usage

1. Choose the format you want to use for the feed:

   [![Rss](https://img.shields.io/badge/rss-F88900?style=for-the-badge&logo=rss&logoColor=white)](https://pwcode.onrender.com/rss)

   [![Atom](https://img.shields.io/badge/Atom-%2366595C.svg?style=for-the-badge&logo=atom&logoColor=white)](https://pwcode.onrender.com/atom)
2. Add the feed URL to your app

## Setting up Local Dev Environment

To set up the local development environment locally, follow these steps:

1. Clone this repository to your local machine.
2. Create a python virtual environment (venv).
2. Install the required dependencies in venv by running:

```bash
pip install -r requirements.txt
```

## Credits

The development of this project would not have been possible without:

- [PapersWithCode API](https://paperswithcode.com/api/v1/docs/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [BS4](https://www.crummy.com/software/BeautifulSoup/)
