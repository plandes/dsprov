"""A stash class used for accessing the provenance of data annotations.

"""
__author__ = 'Paul Landes'

from typing import Dict, Any, List, Iterable
from dataclasses import dataclass, field
import logging
import json
from pathlib import Path
from zensols.persist import persisted, ReadOnlyStash
from zensols.install import Installer
from zensols.nlp import LexicalSpan
from zensols.mimic import Note, HospitalAdmission, Corpus
from . import NoteSpan, NoteMatch, AdmissionMatch

logger = logging.getLogger(__name__)


@dataclass
class AnnotationStash(ReadOnlyStash):
    """A stash that create instances of :class:`.AdmissionMatch`.

    """
    installer: Installer = field()
    corpus: Corpus = field()

    def _parse_match(self, adm: HospitalAdmission, ds_note: Note,
                     match: Dict[str, Any]) -> NoteMatch:
        """Parse discharge summary and note antecedent data."""
        ant_spans: List[NoteSpan] = []
        ds: Dict[str, Any] = match['ds']
        ds_span = NoteSpan(
            lexspan=LexicalSpan(**ds['note_span']),
            note=ds_note)
        ant: Dict[str, Any]
        for ant in match['ant']:
            ant_note: Note = adm.notes_by_id[ant['row_id']]
            ant_spans.append(NoteSpan(
                lexspan=LexicalSpan(**ant['note_span']),
                note=ant_note))
        return NoteMatch(
            hadm_id=adm.hadm_id,
            discharge_summary=ds_span,
            antecedents=tuple(ant_spans),
            source=match)

    def _parse_adm(self, hadm_id: str, anon: Dict[str, Any]) -> AdmissionMatch:
        """Parse matches as a collection into an admission container."""
        note_matches: List[NoteMatch] = []
        adm: HospitalAdmission = self.corpus.get_hospital_adm_by_id(hadm_id)
        matches: Dict[str, Any] = anon['matches']
        ds_note: Note = adm.notes_by_id[anon['ds_row_id']]
        mid: str
        match: Dict[str, Any]
        for mid, match in matches.items():
            note_match: NoteMatch = self._parse_match(adm, ds_note, match)
            note_matches.append(note_match)
        return AdmissionMatch(tuple(note_matches))

    @persisted('_source_anons')
    def _get_source_anons(self) -> Dict[str, Any]:
        """Download the annotations (if not already) and return the JSON content
        as an in memory dict of dicts having roughly the same structure as the
        match object graph.

        """
        self.installer()
        anon_path: Path = self.installer.get_singleton_path()
        if logger.isEnabledFor(logging.DEBUG):
            logger.info(f'parsing {anon_path}')
        with open(anon_path) as f:
            return json.load(f)

    def load(self, hadm_id: str) -> AdmissionMatch:
        sanons: Dict[str, Any] = self._get_source_anons()
        if hadm_id in sanons:
            return self._parse_adm(hadm_id, sanons.get(hadm_id))

    def keys(self) -> Iterable[str]:
        sanons: Dict[str, Any] = self._get_source_anons()
        return sanons.keys()

    def exists(self, hadm_id: str) -> bool:
        sanons: Dict[str, Any] = self._get_source_anons()
        return hadm_id in sanons
