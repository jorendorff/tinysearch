*   the in-memory index
    *   api:
        *   `idx = eensy.Index(dirname)`
        *   `idx.lookup(term) -> [Hit]`
        *   tests based on the eensy sample
    *   schema

            {
                "banana": [      // <---- search term
                    {            // <--- search hits for that term
                        "document": "Banana.txt",
                        "offsets": [0, 1, 4, 9, ...]
                    },
                    {
                        "document": "Fruit.txt",
                        "offsets": [113, 1479, ...]
                    },
                    ...
                ],
                ...
            }

    *   schema implementation
        *   Python learning: namedtuple

    *   loading implementation
        *   tokenization
            *   refinement: lowercasing words
            *   refinement: stop words
            *   refinement: stripping punctuation?
        *   building the data structure

* the search engine
    * api: `idx.search(terms) -> [(filename, score)]` sorted by score descending
    * refinement: tf-idf scores
        * refinement: adjust to avoid overweighting long articles

* the web site
    * python learning: `pyenv` and virtual environments
    * python learning: 2 bits of flask
        * routes
        * templates

* the binary index
    * api:
        * `eensy.create_disk_index(dirname, idx_filename)`
        * `idx = eensy.DiskIndex(idx_filename)`
        * `idx.lookup(term) -> [Hit]`
    * schema
    * build implementation
    * `idx.find` implementation

Queries to show off
* `dogg`
* `waffles`



* mega-refinement: adding support for adjacent words
    * motivation: `hot chicken`
    * This is why the index file contains not only the number of hits
        but their positions.
    * We don't have time to implement. But the first person who can show
        source code and demonstrate this working gets this Hattie B's
        tee! If you're not around, I'll mail it to you. This one is a
        large, but you prefer a different size or color, I get to keep
        this one and buy a new one for you, so, win-win. Unfortunately
        they do not have women's sizes, but what they do have is hoodies
        and delicious food, so you can substitute any one piece of
        Hattie B's merch *or* an unforgettably hot meal for you and a
        friend, on me, *or* I'll give $25 to the charitable organization
        of your choice.

* refinement: show snippets by reloading files

* classic thing about search engines: input is super noisy



Quotes

*   "`True birds first appeared during the [[Cretaceous]] period, around
    {{ma|100| million years ago}}.`"


