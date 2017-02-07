"""A simple search engine in python."""

import re, pathlib, collections, array, struct, csv, math


# === Phase 1: Split text into words

def words(text):
    return re.findall(r"\w+", text.lower())


# === Phase 2: Create an index

Document = collections.namedtuple("Document", "filename size")
Hit = collections.namedtuple("Hit", "doc_id offsets")


def make_index(dir):
    dir = pathlib.Path(dir)
    tiny_dir = dir / ".tiny"
    tiny_dir.mkdir(exist_ok=True)

    # Build the index in memory.
    documents = []
    index = collections.defaultdict(list)  # {str: [Hit]}
    terms = {}  # {str: (int, int)}

    for path in dir.glob("**/*.txt"):
        text = path.read_text()
        doc_words = words(text)
        doc = Document(path.relative_to(dir), len(doc_words))
        doc_id = len(documents)
        documents.append(doc)

        # Build an index for this one document.
        doc_index = collections.defaultdict(
            lambda: Hit(doc_id, array.array('I')))
        for i, word in enumerate(words(text)):
            doc_index[word].offsets.append(i)

        # Merge that into the big index.
        for word, hit in doc_index.items():
            index[word].append(hit)

    # Save the document list.
    with (tiny_dir / "documents.csv").open('w') as f:
        out = csv.writer(f)
        for doc in documents:
            out.writerow(doc)

    # Save the index itself.
    with (tiny_dir / "index.dat").open('wb') as f:
        start = 0
        for word, hits in index.items():
            bytes = b""
            for hit in hits:
                bytes += struct.pack("=II",
                                     hit.doc_id,
                                     len(hit.offsets))
                bytes += hit.offsets.tobytes()
            f.write(bytes)
            terms[word] = (start, len(bytes))
            start += len(bytes)

    # Save the table of terms.
    with (tiny_dir / "terms.csv").open('w') as f:
        out = csv.writer(f)
        for word, (start, length) in terms.items():
            out.writerow([word, start, length])


# === Phase 3: Querying the index

class Index:
    """Object for querying a .tiny index."""

    def __init__(self, dir):
        """Create an Index that reads `$DIR/.tiny`."""
        dir = pathlib.Path(dir)
        tiny_dir = dir / ".tiny"
        self.dir = dir
        self.index_file = tiny_dir / "index.dat"

        self.documents = []
        for [line, max_tf] in csv.reader((tiny_dir / "documents.csv").open('r')):
            self.documents.append(Document(pathlib.Path(line), int(max_tf)))

        self.terms = {}
        for word, start, length in csv.reader((tiny_dir / "terms.csv").open('r')):
            self.terms[word] = (int(start), int(length))

    def lookup(self, word):
        """Return a list of Hits for the given word."""
        if word not in self.terms:
            return []

        start, length = self.terms[word]
        with self.index_file.open('rb') as f:
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

    def lookup_pair(self, first, second):
        """ Return a list of Hits for a pair of words occurring sequentially """
        # Build dictionaries for both words
        first_docs = {hit.doc_id:hit for hit in self.lookup(first)}
        second_docs = {hit.doc_id:hit for hit in self.lookup(second)}

        hits = []
        # Find docs have both words
        for doc_id in set(first_docs.keys()).intersection(set(
                second_docs.keys())):
            first_offsets = set(first_docs[doc_id].offsets)
            # If the second word's offset is one larger than the first word's
            # it occurred immediately after the first word.
            second_offsets = set(offset - 1 for offset in second_docs[
                doc_id].offsets)

            # Find words where the second word occurred after the first one.
            joined_offsets = first_offsets.intersection(second_offsets)

            # Construct a Hit object for the word pair
            if joined_offsets:
                hits.append(Hit(doc_id, sorted(list(joined_offsets))))
        return hits

    def search(self, query):
        """Find documents matching the given query.

        Return a list of (document, score) pairs."""
        scores = collections.defaultdict(float)

        # Find and score the individual words
        word_list = words(query)
        for word in word_list:
            hits = self.lookup(word)
            if hits:
                df = len(hits) / len(self.documents)
                idf = math.log(1 / df)
                for hit in hits:
                    tf = 1000 * len(hit.offsets) / self.documents[hit.doc_id].size
                    scores[hit.doc_id] += tf * idf

        # Find and score word pairs
        for pair in zip(word_list, word_list[1:]):
            hits = self.lookup_pair(*pair)
            if hits:
                df = len(hits) / len(self.documents)
                idf = math.log(1 / df)
                for hit in hits:
                    tf = 1000 * len(hit.offsets) / self.documents[hit.doc_id].size
                    scores[hit.doc_id] += 50 * tf * idf

        results = sorted(scores.items(),
                         key=lambda pair: pair[1],
                         reverse=True)
        return [(self.documents[doc_id].filename, score)
                for doc_id, score in results[:10]]


if __name__ == '__main__':
    import sys
    make_index(sys.argv[1])
