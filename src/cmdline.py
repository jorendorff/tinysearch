import tiny

my_index = tiny.Index("../eensy-sample")

while True:
    query = input("search:> ")
    for doc, score in my_index.search(query):
        print("    {:7.1f} {}".format(score, doc.path))

