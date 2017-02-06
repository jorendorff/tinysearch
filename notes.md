## Intro

Welcome to "A Simple Search Engine in Python".
In the next 45 minutes,
we will write a search engine from scratch.
So grab a laptop or a buddy who types fast.
Go to this URL. Download the tar file.
You'll need it.

Now when we think of search engines,
we all think of the same thing, right?

*(slide: a search box)*

We think of searching the Web.
The Web is big, though,
so today we're going to search a small document set,
just a few thousand Wikipedia articles.
That's what you're downloading right now.

*(slide: listing of Wikipedia articles)*

In fact, we're going to start even smaller than that,
with a subset of just 50 articles.

*(slide: narrowed focus on just a few articles)*

If you've got that file, you can unzip it now
and see what I mean.

    tar xvf ~/Downloads/sample.tar.bz2

This contains two directories.
`small-sample` has 50 articles in it;
`large-sample` has 8,000+.

*(slide: question mark)*

How will our search engine work?

Well, I like to do the dumbest possible thing,
and the dumbest possible search engine is one that simply
scans the full text of every document, every time you enter a query.
User asks for "Tennessee"; it reads every document looking for the word "Tennessee".
In other words, `grep`.

*(slide: grep)*

Everybody loves `grep`.
It's slow, though: it might take a second per thousand Wikipedia articles.
Well, there are millions of Wikipedia articles.
This won't scale. What else can we do?

*(slide: blank)*

We have to transform the data into a shape that's good for fast lookups.
It needs to be less like a pile of text files
and more like a Python dictionary,
so if we look up the word "Tennessee", we get only documents related to Tennessee,
we don't even have to think about all the other junk.

Now there's a word for this:
an arrangement of data, gleaned from text, tuned for finding things.

*(slide: index of a book)*

It's called an index.
The word comes from books.
But relational databases
and search engines use the same word.
It's exactly the same concept in all three.
**An index is metadata that helps you find what you're looking for.**

Real search engines, like Solr and Elasticsearch,
and Google and DuckDuckGo, work by building an index.

Today we'll create an index for 8,000 articles,
and use that index to answer queries.

*(realistically about 4 minutes to this point)*

How are we doing? 41 minutes to go. Right on schedule.

*(slide: architecture)*

Here's what our search engine will look like.
We'll start with the text files.
The first step is to read these files into memory,
and split each one up into words.
Search engines operate on words.

Then we build the index,
which is really just three files on disk.
I'll show what's in these three files in a second.
It's a little hand-coded mini-database.
And that's half the work.
This much happens in one program.
You run that program once, from the command line.
It creates an *index* of all your documents.

The other half of the work is using this data.
We have to write code to look up terms in the index.
We'll take a search query from the user,
we'll use the index to find matching documents,
and assign each document a numeric score
based on how well it matches.
The rest is easy: we just sort the documents by score
and show the top ten results.
All this code on the right
will run in a little Web app we're going to build.

*(slide: index structure)*

What's in the index?

Well, this is what you'd see in the index
if it were a JSON file.
It's pretty simple.
For each word, we have a list of all the search hits for that word.
This shows some search hits for the word *banana*.
It appears in at least two documents.
For every hit, the index has the id of the document,
and the list of places where the word appears in it.
And that's it.

It may not be obvious but this is a *lot* of data.
Our document set contains about 60 million words.
For every single one of them,
our index will contain the location of that word.
So our index will be about 60 million integers big.
Real search indexes are big.
Google's index of the Web is a hundred million gigabytes.

*(7m to here)*

*(slide: index files)*

Let's look even closer at our index.

I said there were three files.
Two small files, one big file.

*   **documents.csv** is a list of the documents
    and how big they are.

    CSV stands for comma separated values.
    This file is just a text file,
    one document per line.

    There are only a few thousand documents,
    so this file is small.

*   **index.dat** is the big one.
    It contains hit data for each word.
    That is, it contains all the document ids and offsets
    that we saw on the previous slide.
    This data is all integers,
    and we're going to store it not as text,
    but as binary data, for efficiency.

    How big is this file?
    60 million integers times 4 bytes per integer,
    that's about a quarter of a gigabyte.
    Plus all the document ids.
    It turns out to be more like half a gigabyte.

*   **terms.csv** is a list of every single word
    that appears in any of the documents, and,
    for every word, the location within `index.dat`
    of all the search hits for that word.
    It's like a table of contents for `index.dat`.

So you can see how this is going to work.
When a user searches for "Tennessee",
first we'll look in `terms.csv`.
That tells us that search hits for "Tennessee"
are located at this offset in `index.dat`.
So then we'll go to `index.dat`
and load up the exact portion of the file that we care about,
just the search hits for "Tennessee".

Those search hits contain document ids and offsets.
The document ids tell us which line of `documents.csv`
to look at, to get filenames.


## Startup

All right. We're making good time.
Create an empty directory.
Mine's called `tiny`.
Unzip those files if you haven't already.

Now open a file `tiny.py`
and let's start stubbing out the parts of our search engine.


*(...)*


## Outro (about 2'00")

### So what?

Takeaways:

*   **Indexes are not magic.**
    "Oh yeah, I see how that works, it's just data."
    I hope that's how you feel about it.
    I like that feeling.

*   **algorithms + data structures = programs.**
    If you're new to Python or you're new to programming:
    this talk is brought to you by Python's
    lists, dictionaries, and named tuples.
    Use them.
    Study them.
    They're so flexible.
    They're so powerful in combination.
    When you understand what it means to build a dictionary
    that maps strings to lists of tuples,
    you can build big ambitious things in 45 minutes.

*   **`pathlib, collections, csv, array, struct,` ...**
    Python's standard library may still contain
    a few surprises for you.


### One more thing

*(make sure `web.py` selects the large sample)*

That's almost eveything.
There is one thing I want your help with.
Let's see what happens if we search for "hot chicken".

These are documents that use the word "hot" many times.
It's sad, because if you use grep,
you'll find out there's one document that uses the exact phrase "hot chicken".
We don't find it.

Likewise, if you search for "batman building",
you get results, but what you don't get
is the one article in our data set that contains the phrase.

Here is my challenge to you.
Our search engine doesn't care about exact phrase matching at all.
But it could.
Fix it.
The information you need is already in the index.
This is why I put offsets in the index.
You can see, hey, document thirty-twelve has "hot" at offset 50
and "chicken" at offset 51.
That means these two words appear right next to each other.
It's an exact phrase match!
And you could award points for that.

This whole repository is on github.
The first pull request I get that fixes this issue,
so that searches for "hot chicken" or "batman building"
find the article that contains those exact phrases,
wins.
And I'm not messing around here.
You will win this fine Hattie B's t-shirt.
This is a large. Not everyone is the same size,
so if you prefer, you can choose this gift certificate --
hot chicken and beer for two.
If you're just visiting here in Nashville, don't miss it.
Or if chicken is not your thing,
I'll donate an equivalent amount of cash
to the charity of your choice.

One MORE thing--
I spent the last year cowriting a book, *Programming Rust.*
If you like this talk, you might like Rust.
For something like a search engine,
a great approach is to prototype in Python
and move to Rust for speed and concurrency.
Anyway, you can pre-order this book
and get early access to 18 chapters right now
at oreilly.com.

OK, ONE MORE THING--
there is another talk about search engines coming up next!
This talk was about how they work inside,
and the goal was to melt your entire brain;
John Berryman's talk is more practical and just as insightful,
he covers tons of stuff I didn't have time for,
and you can catch it in Room 200.

Thank you for coming to see this mess!
It was a blast!
I hope you got some new ideas to pursue.
Thank you.
