## TODO before each performance

* start Firefox in a clean profile
    * start a timer
    * load gist into browser
    * click link to check that it works
    * download sample.tar.bz2 from link
    * get rid of "choose what i share" banner
* close everything else
    * turn off phone
    * close all emacs buffers
    * reset all Terminal tabs
* set up 3 windows
* set font size in Terminal and Emacs (62 cols)
* `rm ~/.pyenv/versions/tiny; rm -rf ~/.pyenv/versions/3.6.0/envs/tiny`
* `mkdir tiny; cd tiny; pyenv local 3.6.0; pyenv virtualenv tiny; pyenv local tiny`
* start QuickTime Player recording screencast


## Talk outline

*   intro
    *   intro proper
    *   scope
    *   architecture diagram
    *   schema (JSON-like)

            {
                "banana": [      # <---- search term
                    {            # <--- search hits for that term
                        "doc_id": 314,    # Banana.txt
                        "offsets": [0, 1, 4, 9, ...]
                    },
                    {
                        "doc_id": 75,     # Fruit.txt
                        "offsets": [113, 1479, ...]
                    },
                    ...
                ],
                ...
            }

*   stubs (API)
    *   two types we will use: `Document`, `Hit`
    *   tokenization (`.split()`)
    *   index creation
    *   lookups
        *   `idx = eensy.Index(dirname)`
        *   `idx.lookup(term) -> [Hit]`
    *   scoring
*   web.py
*   implementation
    *   tokenization (`re.findall()` and `.lower()`)
    *   index creation
        *   building the in-memory form
        *   saving to disk
    *   lookups
        *   this is boring, basically the inverse, paste in code
    *   scoring
        *   basic scoring
        *   adjusting tf for document size (using max_tf)
            *   "two" and "three" and "four" all find Nadal
        *   tf-idf
            *   Motivation: "King of clay" should be Nadal, not Philip II.
                Nadal scores poorly on "of"

*   outro
    *   differences and similarities with the real thing
    *   opportunities
    *   two challenges in particular: 1) how to test this; 2) the "hot chicken" problem


## Most recent run

* stub out tiny.py: 4'55''
* write the flask app: 8'41''
* impl tokenizing: 14'08''
* impl creating the index in memory: 16'00''
* impl writing index to disk (lots of bug-fixing): 26'46''
* show generated files in .tiny: 37'48''
* impl lookup: 39'22''
* better stub out search: 42'59''
* debugging all that: 45'57''
* showing off: 49'12''

SECOND VIDEO
* basic scoring: 0'30''
* fixing & showing off, lots of dead air: 4'19''
* kick off indexing the large sample, lots of stuttering: 5'44''
* control for doc.max_tf: 6'24''
* motivate tf-idf: 9'10''
* impl tf-idf: 10'20''
* done: 13'19''


## TODO

* (by 12a) revise program to match latest run

* trim even more stuff to make it fit in 45 minutes (currently 62'31'')

* tools & testing
    * use static analysis tools
    * hook up emacs static analysis tools
    * subliminal testing?
    * practice switching between keynote and emacs

* gist
    * make single file containing both samples directories
    * upload samples
    * confirm zip doesn't mangle filenames on windows
    * update the code in the gist
    * create bit.ly shortlink to the gist

* intro
    * finish writing intro
    * rehearse intro
    * consider printing intro

* outro
    * rehearse outro
    * print outro

* make slides
    * draw pictures
        * (by 3p) all architecture pictures
    * (by 3p) the index-as-JSON slide
    * (by 3p) the index-for-reals slide

    * the index animation




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
        Hattie B's merch *or* this mouthwatering $25 gift card, *or* if
        you prefer, I'll donate $25 to the charitable organization of
        your choice.

* refinement: show snippets by reloading files

* classic thing about search engines: input is super noisy


## Things to test

*   tokenization
    *   check words lowercased
    *   check treatment of hyphen, apostrophe
    *   check treatment of unicode
*   building
    *   check size of files in .tiny directory
*   index integrity and completeness
    *   every word is in the index
    *   can rebuild each document from index
    *   terms.csv covers the whole range
    *   documents.csv gives correct size of each file
*   lookups and queries
    *   lookups are case-insensitive
    *   lookups that miss
    *   queries that hit on some terms but not others
    *   queries that hit the same document on 2 different terms:
        document appears only once in output
    *   queries that miss completely
    *   junk in queries (filtered out)
    *   query with no words in it (empty result set)
*   scoring
    *   more occurrences, higher rank
    *   larger article does not lead to higher rank
    *   very dumb article repeating a single word does not lead to higher rank
    *   rarer 
*   web site
    *   `GET /` works
    *   `GET /search?q=banana` works
