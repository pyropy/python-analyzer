# Exercism's Python Analyzer

This is Exercism's automated analyzer for the Python track.

It is run with `./bin/analyze.sh $EXERCISM $PATH_TO_FILES` and will write a JSON file with an analysis to the same directory.

For example:

```bash
./bin/analyze.sh two-fer ~/solution-238382y7sds7fsadfasj23j/
```

Unit tests can be run from this directory:

```bash
pylint -x
```
