"""Create and query search indices for text files."""

import array
import collections
import csv
import math
import pathlib
import re
import struct


## === Phase 1: Split text into words

STOP_WORDS = "a an the and of".split()

def words(text):
    return [word for word in re.findall(r"\w+", text.lower()) if word not in STOP_WORDS]


## === Phase 2: Create an index

class Document:
    def __init__(self, path, max_tf=0):
        self.path = path
        self.max_tf = max_tf

Hit = collections.namedtuple("Hit", "doc_id offsets")

def make_index(dir):
    dir = pathlib.Path(dir)
    tiny_dir = dir / ".tiny"
    tiny_dir.mkdir(exist_ok=True)
    documents = [Document(p) for p in sorted(dir.glob("**/*.txt"))]

    # Load all documents into memory.
    index = collections.defaultdict(list)
    for doc_id, doc in enumerate(documents):
        text = doc.path.read_text()

        # Build an index for this one document.
        index_for_doc = collections.defaultdict(lambda: Hit(doc_id, array.array('I')))
        for i, word in enumerate(words(text)):
            index_for_doc[word].offsets.append(i)

        # Record the maximum term frequency.
        doc.max_tf = max(len(hit.offsets) for hit in index_for_doc.values())

        # Merge that into the big index.
        for word, hit in index_for_doc.items():
            index[word].append(hit)

    # Save the document list.
    with open(tiny_dir / "documents.csv", 'w') as f:
        out = csv.writer(f)
        for doc in documents:
            out.writerow([str(doc.path.relative_to(dir)), doc.max_tf])

    # Save the index itself.
    terms = []
    with open(tiny_dir / "index.dat", 'wb') as f:
        start = 0
        for word, hits in index.items():
            bytes = b""
            for hit in hits:
                bytes += struct.pack("=II", hit.doc_id, len(hit.offsets))
                bytes += hit.offsets.tobytes()
            f.write(bytes)
            terms.append((start, len(bytes), word))
            start += len(bytes)

    # Save the table of terms.
    with open(tiny_dir / "terms.csv", 'w') as f:
        out = csv.writer(f)
        for triple in terms:
            out.writerow(triple)


## === Phase 3: Querying the index

class Index:
    def __init__(self, dir):
        dir = pathlib.Path(dir)
        tiny_dir = dir / ".tiny"

        documents = []
        for [line, max_tf] in csv.reader(open(tiny_dir / "documents.csv")):
            documents.append(Document(pathlib.Path(line), int(max_tf)))

        terms = {}
        for start, length, word in csv.reader(open(tiny_dir / "terms.csv")):
            terms[word] = (int(start), int(length))

        self.dir = dir
        self.index_file = tiny_dir / "index.dat"
        self.documents = documents
        self.terms = terms

    def lookup(self, word):
        """Return a list of Hits for the given word."""
        if word not in self.terms:
            return []

        start, length = self.terms[word]
        with open(self.index_file, 'rb') as f:
            f.seek(start)
            bytes = f.read(length)

        read_pos = 0
        hits = []
        while read_pos < len(bytes):
            doc_id, hit_count = struct.unpack("=II", bytes[read_pos:read_pos+8])
            read_pos += 8
            offset_bytes = bytes[read_pos:read_pos + 4 * hit_count]
            read_pos += 4 * hit_count
            offsets = array.array('I')
            offsets.frombytes(offset_bytes)
            hits.append(Hit(doc_id, offsets))
        assert read_pos == len(bytes)
        return hits

    # === Phase 4: Processing search queries and scoring documents

    def search(self, query):
        """Find documents matching the given query.

        Return a list of (document, score) pairs."""
        scores = collections.defaultdict(float)
        for word in words(query):
            hits = self.lookup(word)
            if hits:
                df = len(hits) / len(self.documents)
                idf = math.log(1 / df)
                for hit in hits:
                    tf = 100 * len(hit.offsets) / self.documents[hit.doc_id].max_tf
                    scores[hit.doc_id] += tf * idf

        results = sorted(scores.items(), key=lambda pair: pair[1], reverse=True)
        return [(self.documents[doc_id], score) for doc_id, score in results[:10]]


if __name__ == '__main__':
    import sys
    make_index(sys.argv[1])
