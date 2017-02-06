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
* maximize keynote to its own screen
    * start presentation playing


## Talk outline

*   intro
    *   intro proper
    *   scope
    *   architecture diagram
    *   schema (JSON-like)
    *   file formats
*   stubs (API)
    *   two types we will use: `Document`, `Hit`
    *   tokenization (`.split()`)
    *   index creation
    *   lookups
        *   `idx = eensy.Index(dirname)`
        *   `idx.lookup(term) -> [Hit]`
    *   scoring
*   web.py
    *   demo the web site
    *   (on `/search?q=foo`, check that `foo` appears in the text input!
        if not, you forgot to pass `q=q, results=results` to `render_template`,
        a classic mistake.)
*   implementation
    *   tokenization (`re.findall()` and `.lower()`)
    *   index creation
        *   building the in-memory form
        *   saving to disk
    *   lookups
        *   this is boring, basically the inverse, paste in code
    *   scoring
        *   basic scoring
        *   adjusting tf for document size (using doc.size)
            *   Motivation: "two" and "three" and "four" all find Nadal
        *   tf-idf
            *   Motivation: "King of clay" should be Nadal, not Philip II.
                Nadal scores poorly on "of"
*   outro
    *   differences and similarities with the real thing
    *   opportunities
    *   two challenges in particular: 1) how to test this; 2) the "hot chicken" problem
    *   so what?


## TODO

* trim even more stuff to make it fit in 45 minutes (currently 62'31'')

* tools & testing
    * use static analysis tools
    * hook up emacs static analysis tools
    * subliminal testing?
    * practice switching between keynote and emacs


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
