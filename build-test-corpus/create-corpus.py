# There are about 5889000 entries in the latest dump.
#
# They appear in the order they were created, I think, though the file starts
# with about 16,514 entries in alphabetical order.

import bz2
from xml.etree.ElementTree import iterparse
from pathlib import Path
import collections

# estimated number of articles
ESTIMATE = 5889000

Article = collections.namedtuple("Article", "id title text")

def articles():
    n = 0
    with bz2.BZ2File("articles.xml.bz2", 'r') as infile:
        for event, elem in iterparse(infile, events=("start", "end")):
            if event == 'start':
                if elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}mediawiki':
                    root = elem
            elif event == 'end':
                if elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}page':
                    title_elem = elem.find('{http://www.mediawiki.org/xml/export-0.10/}title')
                    if title_elem is None: continue
                    title = title_elem.text
                    if title is None or ':' in title: continue
                    revision = elem.find('{http://www.mediawiki.org/xml/export-0.10/}revision')
                    if revision is None: continue
                    text_elem = revision.find('{http://www.mediawiki.org/xml/export-0.10/}text')
                    if text_elem is None: continue
                    text = text_elem.text
                    if text is None: continue

                    yield Article(n, title, text)
                    n += 1
                    #if title == 'Zhang Heng':
                    #    break
                root.clear()

for article in articles():
    #if article.id % 1000 == 0:
    if article.title.startswith("AC"):
        print(article.id, article.title, len(article.text))
