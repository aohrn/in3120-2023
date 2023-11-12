#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Iterator, Tuple
from .tokenizer import Tokenizer


class ShingleGenerator(Tokenizer):
    """
    Tokenizes a buffer into overlapping shingles having a specified width. For example, the
    3-shingles for "mouse" are {"mou", "ous", "use"}.

    If the buffer is shorter than the shingle width then this produces a single shorter-than-usual
    shingle.

    The current implementation is simplistic and not whitespace- or punctuation-aware,
    and doesn't treat the beginning or end of the buffer in a special way.
    """

    def __init__(self, width: int):
        assert width > 0
        self.__width = width

    def ranges(self, buffer: str) -> Iterator[Tuple[int, int]]:
        """
        Locates where the shingles begin and end.
        """
        if buffer == "":
            return
        elif len(buffer) <= self.__width:
            yield (0, len(buffer))
        else:
            yield from ((i, i + self.__width) for i in range(0, len(buffer) - self.__width + 1))
