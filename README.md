# Provenience of discharge summaries Pythonic access

[![PyPI][pypi-badge]][pypi-link]
[![Python 3.9][python39-badge]][python39-link]
[![Python 3.10][python310-badge]][python310-link]

This library provides integrated MIMIC-III with discharge summary provenance of
data annotations and Pythonic classes.


## Documentation

See the [full documentation](https://plandes.github.io/dsprov/index.html).
The [API reference](https://plandes.github.io/dsprov/api.html) is also
available.


## Obtaining

The easiest way to install the command line program is via the `pip` installer:
```bash
pip3 install --use-deprecated=legacy-resolver zensols.dsprov
```

Binaries are also available on [pypi].


## Usage

The package includes a command line interface, which is probably most useful by
dumping selected admission annotations.

### Command line

```bash
# help
$ dsprov -h

# get two admission IDs (hadm_id)
$ dsprov ids -l 2

# print out two admissions
$ dsprov show -l 2

# print out admissions 139676
$ dsprov show -d 139676

# output the JSON of two admissions with indent 4
$ dsprov show -i 4 -f json -d $(dsprov ids -l 2 | awk '{print $1}' | paste -s -d, -)
```

### API

The package can be used directly in your research to provide Python object
oriented access to the annotations:

```python
>>> from zensols.nlp import FeatureDocument
>>> from zensols.dsprov import ApplicationFactory, AdmissionMatch
>>> stash = ApplicationFactory.get_stash()
>>> am: AdmissionMatch = next(iter(stash.values()))
>>> doc: FeatureDocument = am.note_matches[0].discharge_summary.note.doc
>>> print(f'hadm: {am.hadm_id}')
>>> print(f'sentences: {len(doc.sents)}')
>>> print(f'tokens: {doc.token_len}')
>>> print(f'entities: {doc.entities}')
hadm: 120334
sentences: 46
tokens: 1039
entities: (<Admission>, <Date>, <Discharge>, <Date>, <Date of Birth>, <Sex>, ...)
```

## Docker

A [docker](docker/app/README.md) image is available as well.

To use the docker image, do the following:

1. Create (or obtain) the [Postgres docker image]
1. Clone this repository `git clone --recurse-submodules
   https://github.com/plandes/dsprov`
1. Set the working directory to the repo: `cd dsprov`
1. Copy the configuration from the installed [mimicdb] image configuration:
   `make -C docker/mimicdb SRC_DIR=<cloned mimicdb directory> cpconfig`
1. Start the container: `make -C docker/app up`
1. Test sectioning a document: `make -C docker/app testdumpsec`
1. Log in to the container: `make -C docker/app devlogin`


## Changelog

An extensive changelog is available [here](CHANGELOG.md).


## License

[MIT License](LICENSE.md)

Copyright (c) 2023 Paul Landes


<!-- links -->
[pypi]: https://pypi.org/project/zensols.dsprov/
[pypi-link]: https://pypi.python.org/pypi/zensols.dsprov
[pypi-badge]: https://img.shields.io/pypi/v/zensols.dsprov.svg
[python39-badge]: https://img.shields.io/badge/python-3.9-blue.svg
[python39-link]: https://www.python.org/downloads/release/python-390
[python310-badge]: https://img.shields.io/badge/python-3.10-blue.svg
[python310-link]: https://www.python.org/downloads/release/python-310
