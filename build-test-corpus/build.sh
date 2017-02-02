set -e -

# URL of the latest dump. This links to a current Wikipedia mirror,
# so if the URL goes bad, try changing "wikimedia.your.org" to just "wikimedia.org".
URL=http://dumps.wikimedia.your.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2

# What we're going to call that file when we download it.
DUMPFILE=`basename "${URL}"`

cd `dirname $0`/..

# Where we want to create our output.
OUTDIR=large-sample

# Names of the bundles we want to create.
ZIPFILE=large-sample.zip
TARFILE=large-sample.tar.bz2

### # Download the latest dump. Could not figure out how to configure wget to do this
### # in any reasonable way, so we just re-download the whole thing every time.
### # TODO: write a Makefile instead.
### ### (cd build-test-corpus && wget "${URL}")
###
### # Run the program that creates the files.
### build-test-corpus/create-corpus.py "build-test-corpus/${DUMPFILE}" "${OUTDIR}"

# In case we've run the program before.
rm -rf "${OUTDIR}/.tiny"

# Build the zipfile.
zip -r "${ZIPFILE}" "${OUTDIR}"

# Build the tarfile.
tar cvjf "${TARFILE}" "${OUTDIR}"

