# This code was originally provided as precode for IN2110 V21.
# It has been modified for IN3120 H23 to increase difficulty and redistributed
# under the concept of "det er lettere å be om tilvgivelse enn tillatelse".
# - oliverrj@ifi, 2023-10-26
####

# /////////

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from collections import Counter
import math
import nltk


class Chatbot:
    """Retrieval-based chatbot using TF-IDF vectors"""

    def __init__(self, dialogue_file):
        """Given a corpus of dialoge utterances (one per line), computes the
        document frequencies and TF-IDF vectors for each utterance"""

        # We store all utterances (as lists of lowercased tokens)
        self.utterances = []
        fd = open(dialogue_file)
        for line in fd:
            utterance = self._tokenise(line.rstrip("\n"))
            self.utterances.append(utterance)
        fd.close()

        self.doc_freqs = self._compute_doc_frequencies()
        self.tf_idfs = [self.get_tf_idf(utterance) for utterance in self.utterances]

    def _tokenise(self, utterance):
        """Convert an utterance to lowercase and tokenise it by using the toknization of your choice"""
        return utterance.lower().split()
        return nltk.word_tokenize(utterance.lower())

    def _compute_doc_frequencies(self):
        """Compute the document frequencies (necessary for IDF)"""
        doc_freqs = {}
        for utterance in self.utterances:
            for token in utterance:
                doc_freqs[token] = doc_freqs.get(token, 0) + 1
        return doc_freqs

    def get_tf_idf(self, utterance):
        """Compute the TF-IDF vector of an utterance. The vector can be represented
        as a dictionary mapping words to TF-IDF scores."""
        tf_idf_dict = {}
        term_counts = Counter(utterance)
        for term, freq in term_counts.items():
            idf = math.log(len(self.utterances) / (self.doc_freqs.get(term, 0) + 1))
            tf_idf_dict[term] = freq * idf

        return tf_idf_dict

    def _get_norm(self, tf_idf):
        """Computes the norm of a vector"""
        norm = 0
        for word in tf_idf:
            norm += tf_idf[word] ** 2
        return norm**0.5

    def compute_cosine(self, tf_idf1, tf_idf2):
        """Computes the cosine similarity between two vectors"""
        dot_product = 0
        for word in tf_idf1:
            if word in tf_idf2:
                dot_product += tf_idf1[word] * tf_idf2[word]
        norm1 = self._get_norm(tf_idf1)
        norm2 = self._get_norm(tf_idf2)
        return dot_product / (norm1 * norm2)

    def get_response(self, query):
        """
        Finds out the utterance in the corpus that is closed to the query
        (based on cosine similarity with TF-IDF vectors) and returns the
        utterance following it.
        """

        # If the query is a string, we first tokenise it
        query_tokens = type(query) == str and self._tokenise(query) or query

        # Vectorize the query
        query_vector = self.get_tf_idf(query_tokens)

        # Init variables for storing max cosine and index of best match
        max_cosine, max_idx = 0, 0

        # Evaluate all other documents as potential matches
        for i, tf_idf in enumerate(self.tf_idfs):
            # calculate candidate cosine similarity
            cos = self.compute_cosine(query_vector, tf_idf)
            # If this is the best match so far, update the variables
            if cos > max_cosine:
                max_cosine = cos
                max_idx = i
        # Return the utterance following the best match
        # TODO: Implement better output formatting in regard to punctuation
        return " ".join(self.utterances[max_idx + 1])


if __name__ == "__main__":
    TEST_SENTS = [
        "hello world",
        "Who are you?",
        "I am a chatbot",
        "What is the meaning of stonehenge?",
    ]
    cb = Chatbot("lotr.en")

    for sent in TEST_SENTS:
        print("--------")
        print(sent)
        print(cb.get_response(sent))
        print("--------")
