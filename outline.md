## Talk outline

*   intro
    *   intro proper
    *   scope
    *   architecture diagram
    *   schema (as JSON)

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

*   stubs (API)
    *   tokenization
    *   index creation
    *   lookups
        *   `idx = eensy.Index(dirname)`
        *   `idx.lookup(term) -> [Hit]`
    *   scoring
    *   presentation
*   implementation
*   outro
    *   two challenges: 1) how to test this; 2) the "hot chicken" problem



## TODO

* upload samples
* use static analysis tools
* hook up emacs static analysis tools
* subliminal testing?
* practice switching between keynote and emacs
* practice comparing wdir to particular git revisions, as insurance
* create the gist
* create bit.ly shortlink to the gist
* is emacs always on the screen?


## TODO before each performance

* start Firefox in a clean profile
* close everything else
* clone the github repo
* and delete all files
* create an area on the screen for the gist link
* set font size in Terminal and Emacs


## Old outline

*   the in-memory index
    *   api:
        *   tests based on the eensy sample
    *   schema
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


