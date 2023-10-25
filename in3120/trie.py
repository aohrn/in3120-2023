#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import Dict, List, Optional, Iterable, Iterator
from .tokenizer import Tokenizer


class Trie:
    """
    A very simple and straightforward implementation of a trie for demonstration purposes
    and tiny dictionaries. A node in the trie is also itself a trie in this implementation.

    A serious real-world implementation of a trie or an automaton would not be implemented
    this way. The trie/automaton would then instead be encoded into a single contiguous buffer
    and there'd be significant attention on memory consumption and scalability with respect to
    dictionary size.

    Using, e.g., Marisa (https://github.com/pytries/marisa-trie), or DAWG (https://dawg.readthedocs.io/en/latest/),
    or datrie (https://pypi.org/project/datrie/), or hat-trie (https://github.com/pytries/hat-trie)
    would have plausible open source alternatives.

    The current implementation does not support associating a value of some kind (say, an integer)
    with each string added to the trie. Support for this can be trivially added, though, if needed.
    Some applications might benefit from this, if we need to keep rich metadata associated with each
    string. In such cases, these associated values can be used as lookup keys into, e.g., some
    external database.
    """

    def __init__(self):
        self.__children: Dict[str, Optional[Trie]] = {}

    def __repr__(self):
        return repr(self.__children)

    def __contains__(self, string: str):
        descendant = self.consume(string)
        return descendant is not None and descendant.is_final()

    def __iter__(self):
        return self.strings()

    def __getitem__(self, prefix: str):
        return self.consume(prefix)

    def __add(self, string: str) -> None:
        assert 0 < len(string)
        trie = self
        for symbol in string:
            if symbol not in trie.__children:
                trie.__children[symbol] = Trie()
            trie = trie.__children[symbol]
        trie.__children[""] = None

    def add(self, strings: Iterable[str], tokenizer: Tokenizer) -> None:
        """
        Adds all the strings to the trie. The tokenizer is used so that we're robust
        to nuances in whitespace and punctuation. Use the same tokenizer throughout.
        """
        # TODO: Make the tokenizer a class variable.
        for string in strings:
            self.__add(" ".join(tokenizer.strings(string)))

    def consume(self, prefix: str) -> Optional[Trie]:
        """
        Consumes the given prefix verbatim and returns the resulting descendant node,
        if any. I.e., if strings that have this prefix have been added to the trie, then
        the trie node corresponding to traversing the prefix is returned. Otherwise, None
        is returned.
        """
        node = self
        for symbol in prefix:
            node = node.__children.get(symbol, None)
            if not node:
                return None
        return node

    def child(self, transition: str) -> Optional[Trie]:
        """
        Returns the immediate child node, given a transition symbol. Returns None if the transition
        symbol is invalid. Functionally equivalent to consume(transition), but simpler and for the
        special of a single transition symbol and not a longer string.
        """
        return self.__children.get(transition, None)

    def strings(self) -> Iterator[str]:
        """
        Yields all strings that are found in or below this node. For simple testing and debugging purposes.
        The returned strings are emitted back in lexicographical order.
        """
        stack = [(self, "")]
        while stack:
            node, prefix = stack.pop()
            if node.is_final():
                yield prefix
            for symbol, child in sorted(node.__children.items(), reverse=True):
                if child:
                    stack.append((child, prefix + symbol))

    def transitions(self) -> List[str]:
        """
        Returns the set of symbols that are valid outgoing transitions, i.e., the set of symbols that
        when consumed by this node would lead to a valid child node. The returned transitions are
        emitted back in lexicographical order.
        """
        return sorted(s for s in self.__children if s)

    def is_final(self) -> bool:
        """
        Returns True iff the current node is a final/terminal state in the trie/automaton, i.e.,
        if a string has been added to the trie where the end of the string ends up in this node.
        """
        return "" in self.__children
