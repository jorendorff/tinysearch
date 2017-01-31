import eensy

my_index = eensy.Index("../eensy-sample")
while True:
    search_query = input("?> ")
    for doc, score in my_index.search(search_query, 10):
        print("{:7.1f} {}".format(score, doc.name))
