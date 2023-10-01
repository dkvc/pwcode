# PapersWithCode Latest (pwcode)

## Get Latest Updates from PapersWithCode

This module allows you to deploy your own local server that retrieves latest PapersWithCode papers. You can also use web server hosted by us on [Render](https://pwcode.onrender.com/latest). The information can be retrieved in the form of [JSON](https://pwcode.onrender.com/latest), [RSS](https://pwcode.onrender.com/rss) or [Atom](https://pwcode.onrender.com/atom) feeds. All formats consist of the same data and are updated at the same time.

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/dkvc/pwcode/main.svg)](https://results.pre-commit.ci/latest/github/dkvc/pwcode/main)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000)](https://github.com/psf/black)

## Usage

To add the PapersWithCode feed to your feeder app, follow these steps:

1. Choose the format you want to use for the feed:
    - JSON
    - RSS
    - Atom
2. Add the feed URL to your app

## Setting up Local Dev Environment

To set up the local development environment locally, follow these steps:

1. Clone this repository to your local machine.
2. Install the required dependencies by running:

```bash
pip install -r requirements.txt
```

## Credits

This project is made possible by :

- PapersWithCode own API
- FastAPI