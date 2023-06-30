"""Container classes for discharge summary to note antecedent match data.

"""
__author__ = 'Paul Landes'

from typing import ClassVar, Tuple, Dict, Any
from dataclasses import dataclass, field
import sys
from io import TextIOBase
from collections import OrderedDict
import textwrap as tw
from zensols.config import Dictable
from zensols.persist import persisted
from zensols.nlp import LexicalSpan, TokenContainer, FeatureSpan
from zensols.mimic import Note, Section


@dataclass
class MatchBase(Dictable):
    """A base class for match data containers that enforces no
    pickling/serialization of note spans.  This is not supported as subclasses
    contain complex object graphs.

    """
    def __getstate__(self):
        raise ValueError('Pickeling not supported')

    def repr(self) -> str:
        return self.__str__()


@dataclass
class NoteSpan(MatchBase):
    """A *tie* between two spans of semantically similar or copied text segments
    between a note antecedent and a discharge summary This is the analog to
    ``MatchedNote`` in the reproducibility repo, but use paper terminology.

    """
    lexspan: LexicalSpan = field()
    """The 0-index start and end offset in :obj:`note` the demarcates the span
    lexically.

    """
    note: Note = field()
    """The note that matches."""

    @property
    def text(self) -> str:
        """The span as text demarcated by the span."""
        return self.note.text[self.lexspan.begin:self.lexspan.end]

    @property
    def norm_text(self) -> str:
        """The normalized as the span text spaced and without newlines."""
        toks = filter(lambda t: not t.is_space, self.span.token_iter())
        span = FeatureSpan(tokens=tuple(toks))
        return span.norm

    @property
    def span(self) -> TokenContainer:
        """The span as features demarcated by the span."""
        return self.note.doc.get_overlapping_span(self.lexspan)

    @property
    @persisted('_sections')
    def sections(self) -> Dict[int, Section]:
        """The sections coverd by the span."""
        overlaps: Dict[int, Section] = {}
        i: int
        sec: Section
        for i, sec in self.note.sections.items():
            if sec.lexspan.overlaps_with(self.lexspan):
                overlaps[i] = sec
        return overlaps

    def write(self, depth: int = 0, writer: TextIOBase = sys.stdout,
              include_sections: bool = False):
        if include_sections:
            self._write_line('text:', depth, writer)
            self._write_block(self.text, depth + 1, writer)
            self._write_line('sections:', depth, writer)
            for i, sec in sorted(self.sections.items(), key=lambda t: t[0]):
                self._write_line(str(sec), depth + 1, writer)
        else:
            self._write_block(self.text, depth, writer)

    def _from_dictable(self, *args, **kwargs) -> Dict[str, Any]:
        return OrderedDict(
            [['row_id', self.note.row_id],
             ['span', self.lexspan.asdict()],
             ['text', self.text]])

    def __str__(self) -> str:
        return str(self.note)


@dataclass
class NoteMatch(MatchBase):
    """A match between a text span in the discharge summary with the semanically
    similar or copy/pasted text with the note antecedents.  This is the analog
    to the ``MatchedAnnotation`` in the reproducibility repo.

    """
    STR_SPAN_WIDTH: ClassVar[int] = 30

    hadm_id: int = field()
    """The admission unique identifier."""

    discharge_summary: NoteSpan = field()
    """The discharge summary note and span."""

    antecedents: Tuple[NoteSpan] = field()
    """The note antecedent note/spans."""

    source: Dict[str, Any] = field()
    """The source annotation JSON that was used to construct this instance."""

    def write(self, depth: int = 0, writer: TextIOBase = sys.stdout,
              include_sections: bool = False):
        did: str = self.discharge_summary.note.row_id
        self._write_line(f'discharge summary ({did}):', depth, writer)
        self.discharge_summary.write(depth + 1, writer, include_sections)
        if len(self.antecedents) == 1:
            aid: str = self.antecedents[0].note.row_id
            self._write_line(f'antecedent ({aid}):', depth, writer)
            self.antecedents[0].write(depth + 1, writer, include_sections)
        else:
            self._write_line('antecedents:', depth, writer)
            ant: NoteSpan
            for ant in self.antecedents:
                aid: str = self.antecedents[0].note.row_id
                self._write_line(f'{aid}:', depth + 1, writer)
                ant.write(depth + 2, writer, include_sections)

    def desc(self, width: int) -> str:
        """A short description string of the match."""
        def shorten(span: NoteSpan) -> str:
            s: str = tw.shorten(span.text, width=width)
            return f'({span.note.row_id}) {s}'

        width = self.STR_SPAN_WIDTH
        ds: str = shorten(self.discharge_summary)
        ants: str = ', '.join(map(shorten, self.antecedents))
        return f'{self.hadm_id}: {ds} -> {ants}'

    def _from_dictable(self, *args, **kwargs) -> Dict[str, Any]:
        return OrderedDict(
            [['ds', self.discharge_summary.asdict()],
             ['ant', tuple(map(lambda a: a.asdict(), self.antecedents))]])

    def __str__(self) -> str:
        return self.desc(self.STR_SPAN_WIDTH)


@dataclass
class AdmissionMatch(MatchBase):
    """Contains match data for an admission.

    """
    _DICTABLE_WRITABLE_DESCENDANTS: ClassVar[bool] = True

    note_matches: Tuple[NoteMatch] = field()
    """Contains match data for notes."""

    @property
    def hadm_id(self) -> int:
        """The admission unique identifier."""
        return self.note_matches[0].hadm_id

    def write(self, depth: int = 0, writer: TextIOBase = sys.stdout):
        nm: NoteMatch
        self._write_line(f'{self}', depth, writer)
        for i, nm in enumerate(self.note_matches):
            if i > 0:
                self._write_divider(depth, writer)
            self._write_object(nm, depth, writer)

    def __str__(self) -> str:
        return f'{self.hadm_id}: {len(self.note_matches)} matches'
