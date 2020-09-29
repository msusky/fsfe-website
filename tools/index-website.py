# SPDX-FileCopyrightText: 2020 Free Software Foundation Europe e.V. <https://fsfe.org>
# SPDX-License-Identifier: GPL-3.0-or-later

# Build an index for the search engine based on the article titles and tags

import glob
import json
from bs4 import BeautifulSoup

articles = []

for file in list(
    glob.glob("about/**/*.xhtml")
    + glob.glob("activities/**/*.xhtml")
    + glob.glob("news/**/*.xhtml"),
):
    with open(file, "r", encoding=("utf-8")) as file_fh:
        file_parsed = BeautifulSoup(file_fh.read(), "lxml")
        tags = [
            tag.get("key")
            for tag in file_parsed.find_all("tag")
            if tag.get("key") != "front-page"
        ]
        articles.append(
            {
                "url": "https://fsfe.org/" + file.replace("xhtml", "html"),
                "tags": " ".join(tags),
                "title": file_parsed.title.text,
            }
        )

# Make a JS file that can be directly loaded
# TODO find an easy way to load local JSON file from JavaScript
with open("search/index.js", "w", encoding="utf-8") as fh:
    fh.write("var posts = " + json.dumps(articles, ensure_ascii=False))
