# pylint: disable=missing-module-docstring
# pylint: disable=line-too-long

import math
from collections import Counter
from typing import Any, Dict, Iterable, Iterator
from .dictionary import InMemoryDictionary
from .normalizer import Normalizer
from .tokenizer import Tokenizer
from .corpus import Corpus


class NaiveBayesClassifier:
    """
    Defines a multinomial naive Bayes text classifier.
    """

    def __init__(self, training_set: Dict[str, Corpus], fields: Iterable[str],
                 normalizer: Normalizer, tokenizer: Tokenizer):
        """
        Constructor. Trains the classifier from the named fields in the documents in
        the given training set.
        """
        # Used for breaking the text up into discrete classification features.
        self.__normalizer = normalizer
        self.__tokenizer = tokenizer

        # The vocabulary we've seen during training.
        self.__vocabulary = InMemoryDictionary()

        # Maps a category c to the prior probability Pr(c).
        self.__priors: Dict[str, float] = {}

        # Maps a category c and a term t to the conditional probability Pr(t | c).
        self.__conditionals: Dict[str, Dict[str, float]] = {}

        # Maps a category c to the denominator used when doing Laplace smoothing.
        self.__denominators: Dict[str, int] = {}

        # Train the classifier, i.e., estimate all probabilities.
        self.__compute_priors(training_set)
        self.__compute_vocabulary(training_set, fields)
        self.__compute_posteriors(training_set, fields)

    def __compute_priors(self, training_set) -> None:
        """
        Estimates all prior probabilities needed for the naive Bayes classifier.
        """
        # Maximum likelihood estimate.
        total_count = sum(map(len, training_set.values()))
        self.__priors = {category: corpus.size() / total_count for category, corpus in training_set.items()}

    def __compute_vocabulary(self, training_set, fields) -> None:
        """
        Builds up the overall vocabulary as seen in the training set.
        """
        # We're doing simple add-one (Laplace) smoothing when estimating the probabilities, so
        # figure out the size of the overall vocabulary.
        for _, corpus in training_set.items():
            for document in corpus:
                for field in fields:
                    for term in self.__get_terms(document.get_field(field, "")):
                        self.__vocabulary.add_if_absent(term)

    def __compute_posteriors(self, training_set, fields) -> None:
        """
        Estimates all conditional probabilities needed for the naive Bayes classifier.
        """
        # Use smoothed estimates. Remember the denominators we used, so that we later know how
        # to deal with terms we haven't seen for a category.
        for category, corpus in training_set.items():
            terms = self.__get_terms(" ".join(d.get_field(f, "") for d in corpus for f in fields))
            term_frequencies = Counter(terms)
            self.__denominators[category] = sum(term_frequencies.values()) + self.__vocabulary.size()
            self.__conditionals[category] = {term: (freq + 1) / self.__denominators[category]
                                             for term, freq in term_frequencies.items()}

    def __get_terms(self, buffer) -> Iterator[str]:
        """
        Processes the given text buffer and returns the sequence of normalized
        terms as they appear. Both the documents in the training set and the buffers
        we classify need to be identically processed.
        """
        tokens = self.__tokenizer.strings(self.__normalizer.canonicalize(buffer))
        return (self.__normalizer.normalize(t) for t in tokens)

    def classify(self, buffer: str) -> Iterator[Dict[str, Any]]:
        """
        Classifies the given buffer according to the multinomial naive Bayes rule. The computed (score, category) pairs
        are emitted back to the client via the supplied callback sorted according to the scores. The reported scores
        are log-probabilities, to minimize numerical underflow issues. Logarithms are base e.

        The results yielded back to the client are dictionaries having the keys "score" (float) and
        "category" (str).
        """
        # Only consider terms that occurred in the training set, for any category.
        terms = [term for term in self.__get_terms(buffer) if term in self.__vocabulary]

        # Seed with priors.
        scores = {category: math.log(prior) for category, prior in self.__priors.items()}

        # Accumulate log-probabilities for each term. For terms not observed for the current category,
        # use a smoothed estimate.
        for category in scores:
            default = 1.0 / self.__denominators[category]
            for term in terms:
                scores[category] += math.log(self.__conditionals[category].get(term, default))

        # Emit categories back to the client in sorted order.
        for category, score in sorted(scores.items(), key=lambda pair: pair[1], reverse=True):
            yield {"score": score, "category": category}
