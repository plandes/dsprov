# Provenience of discharge summaries Pythonic access

[![PyPI][pypi-badge]][pypi-link]
[![Python 3.9][python39-badge]][python39-link]
[![Python 3.10][python310-badge]][python310-link]

This library provides integrated MIMIC-III with discharge summary provenance of
data annotations and Pythonic classes.  This is a package meant for other
researchers based on the paper [Hospital Discharge Summarization Data
Provenance](https://aclanthology.org/2023.bionlp-1.41/).


## Documentation

See the [full documentation](https://plandes.github.io/dsprov/index.html).
The [API reference](https://plandes.github.io/dsprov/api.html) is also
available.


## Installation and Configuration

Both the package and database must be installed.


### Package

The library can be installed with pip from the [pypi] repository:
```bash
pip3 install --use-deprecated=legacy-resolver zensols.dsprov
```
The `--use-deprecated=legacy-resolver` is needed for the spaCy 3.2 dependency.
Python version 3.10 must also be used since it depends on PyTorch 1.13 (at
least for the binary packages).


### Database

The MIMIC-III database must be installed and configured as documented in the
[mimic package's configuration], which is necessary to render the EHR data used
by the annotations.  However, instead of using `~/.mimicrc`, the file must be
called `~/.dsprovrc` if not explicitly set with the `--config` option..  The
[mimic package's configuration] section also provides instructions on how to
install a MIMIC-III database via PostgreSQL, SQLite or in a Docker container.

For example, to store cached files in `~/.dsprov/cache` using a the SQLite
MIMIC-III database file `~/.dsprov/cache/mimic3.sqlite3`, your `~/.dsprovrc`
would be:
```ini
[default]
# the directory where cached data is stored
data_dir = ~/.dsprov/cache

[mimic_sqlite_conn_manager]
# location of the MIMIC-III SQLite database file
db_file = path: ~/.dsprov/cache/mimic3.sqlite3
```


## Usage

The package includes a command line interface, which is probably most useful by
dumping selected admission annotations.


### Command line

```bash
# help
$ dsprov --help

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
1. Copy the configuration from the installed [mimicdb] image
   configuration: `make -C docker/mimicdb SRC_DIR=<cloned mimicdb directory>
   cpconfig`
1. Start the container: `make -C docker/app up`
1. Test sectioning a document: `make -C docker/app testdumpsec`
1. Log in to the container: `make -C docker/app devlogin`


## Citation

If you use this project in your research please use the following BibTeX entry:

```bibtex
@inproceedings{landesHospitalDischargeSummarization2023,
  title = {Hospital {{Discharge Summarization Data Provenance}}},
  booktitle = {The 22nd {{Workshop}} on {{Biomedical Natural Language Processing}} and {{BioNLP Shared Tasks}}},
  author = {Landes, Paul and Chaise, Aaron and Patel, Kunal and Huang, Sean and Di Eugenio, Barbara},
  date = {2023-07},
  pages = {439--448},
  publisher = {{Association for Computational Linguistics}},
  location = {{Toronto, Canada}},
  url = {https://aclanthology.org/2023.bionlp-1.41},
  urldate = {2023-07-10},
  eventtitle = {{{BioNLP}} 2023}
}
```

Also please cite the [Zensols Framework]:

```bibtex
@article{Landes_DiEugenio_Caragea_2021,
  title={DeepZensols: Deep Natural Language Processing Framework},
  url={http://arxiv.org/abs/2109.03383},
  note={arXiv: 2109.03383},
  journal={arXiv:2109.03383 [cs]},
  author={Landes, Paul and Di Eugenio, Barbara and Caragea, Cornelia},
  year={2021},
  month={Sep}
}
```


## Changelog

An extensive changelog is available [here](CHANGELOG.md).


## License

[MIT License](LICENSE.md)

Copyright (c) 2023 - 2024 Paul Landes


<!-- links -->
[pypi]: https://pypi.org/project/zensols.dsprov/
[pypi-link]: https://pypi.python.org/pypi/zensols.dsprov
[pypi-badge]: https://img.shields.io/pypi/v/zensols.dsprov.svg
[python39-badge]: https://img.shields.io/badge/python-3.9-blue.svg
[python39-link]: https://www.python.org/downloads/release/python-390
[python310-badge]: https://img.shields.io/badge/python-3.10-blue.svg
[python310-link]: https://www.python.org/downloads/release/python-310

[Zensols Framework]: https://github.com/plandes/deepnlp
[Postgres docker image]: https://github.com/MIT-LCP/mimic-code/blob/main/mimic-iii/buildmimic/postgres/README.md
[mimic package's configuration]: https://github.com/plandes/mimic#configuration
[mimicdb]: https://github.com/plandes/mimicdb
