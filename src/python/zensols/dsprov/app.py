"""This library provides integrated MIMIC-III with discharge summary provenance
of data annotations and Pythonic classes.

"""
__author__ = 'Paul Landes'

from typing import Dict, Any, Iterable, List, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
import logging
import sys
import json
import yaml
import itertools as it
from zensols.persist import Stash
from zensols.cli import ApplicationError
from . import AdmissionMatch

logger = logging.getLogger(__name__)


class Format(Enum):
    text = auto()
    json = auto()
    yaml = auto()


@dataclass
class Application(object):
    """This library provides integrated MIMIC-III with discharge summary
    provenance of data annotations and Pythonic classes.

    """
    stash: Stash = field()
    """A stash that creates :class:`.AdmissionMatch` instances."""

    def admissions(self, limit: int = None):
        """Print the annotated admission IDs.

        :param limit: the limit on items to print

        """
        limit = sys.maxsize if limit is None else limit
        k: str
        for k in it.islice(self.stash.keys(), limit):
            print(k)

    def show(self, limit: int = None, format: Format = Format.text,
             ids: str = None, indent: int = None):
        """Print annotated matches

        :param limit: the limit on items to print

        :param format: the output format

        :param ids: a comma separated list of hospital admission IDs (hadm_id)

        :param indent: the indentation (if any)

        """
        limit = sys.maxsize if limit is None else limit
        ams: Iterable[AdmissionMatch]
        if ids is None:
            ams = it.islice(self.stash, limit)
        else:
            ams: List[Tuple[str, AdmissionMatch]] = []
            for aid in ids.split(','):
                if aid not in self.stash:
                    raise ApplicationError(
                        f'Admission (hadm_id) does not exist: {aid}')
                ams.append((aid, self.stash[aid]))
        if format == Format.text:
            for ix, (i, am) in enumerate(ams):
                if ix > 0:
                    print('=' * 80)
                am.write()
        else:
            dct: Dict[str, Any] = dict(
                map(lambda t: (t[0], t[1].asflatdict()['note_matches']), ams))
            if format == Format.json:
                print(json.dumps(dct, indent=indent))
            elif format == Format.yaml:
                print(yaml.dump(dct))
