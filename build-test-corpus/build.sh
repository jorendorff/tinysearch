set -e -

# URL of the latest dump. This links to a current Wikipedia mirror,
# so if the URL goes bad, try changing "wikimedia.your.org" to just "wikimedia.org".
URL=http://dumps.wikimedia.your.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2

# What we're going to call that file when we download it.
DUMPFILE=`basename "$URL"`

cd `dirname $0`/..

# Where we want to create our output.
OUTDIR=large-sample
SMALL_OUTDIR=small-sample

### # Download the latest dump. Could not figure out how to configure wget to do this
### # in any reasonable way, so we just re-download the whole thing every time.
### # TODO: write a Makefile instead.
### ### (cd build-test-corpus && wget "$URL")
### xattr -d com.apple.quarantine "$DUMPFILE"
###
### # Run the program that creates the files.
### build-test-corpus/create-corpus.py "build-test-corpus/$DUMPFILE" "$OUTDIR"


# In case we've run the program before.
rm -rf "small-sample/.tiny"
rm -rf "large-sample/.tiny"

# Create zip bundle.
ZIP_BUNDLE=sample.zip
rm -f "$ZIP_BUNDLE"
zip -r "$ZIP_BUNDLE" small-sample large-sample

# Create tarball.
TAR_BUNDLE=sample.tar.bz2
tar cjf "$TAR_BUNDLE" small-sample large-sample
