import tiny, sys

my_index = tiny.Index(sys.argv[1])

while True:
    query = input("search:> ")
    for doc, score in my_index.search(query):
        print("    {:7.1f} {}".format(score, doc.path))

