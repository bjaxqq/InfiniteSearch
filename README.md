# InfiniteSearch

This is a very basic recipe scraper for the popular web game [Infinite Craft](https://neal.fun/infinite-craft/) created by Neal Agarwal.

## Installation

Since this script uses various packages, your machine may not have them already installed. To do so, you can run:

```bash
git clone https://github.com/bjaxqq/InfiniteSearch
pip3 install -r requirements.txt
```

## Usage

After finishing the installation process, you can now run:

```bash
python3 craft.py
```

This will create a JSON file called `crafts.json` which will be used to store all of the data from the scrape. There are future plans to create an external interface to search for different crafts, perhaps in the form of a browser extension, but for now you will just have to search through the JSON file itself.