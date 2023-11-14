####
# This code was originally provided as a solution sketch for IN2110 V21.
# It has been modified and redistributed for IN3120 H23 under the concept of
# "det er lettere å be om tilvgivelse enn tillatelse". It will be unpublished
# before IN2110 V24.
# - oliverrj@ifi, 2023-10-27
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

"""The file contains two implementations:
1) A method to compute BLEU scores

2) A retrieval-based chatbot based on TF-IDF. 
"""


import math
import numpy as np


class Chatbot:
    """Retrieval-based chatbot using TF-IDF vectors"""

    def __init__(self, dialogue_file):
        """Given a corpus of dialoge utterances (one per line), computes the
        document frequencies and TF-IDF vectors for each utterance"""

        # We store all utterances (as lists of lowercased tokens)
        self.utterances = []
        fd = open(dialogue_file)
        for line in fd:
            self.utterances.append(line.lower().rstrip("\n").split())
        fd.close()

        self.doc_freqs = self._compute_doc_frequencies()
        self.tf_idfs = [self.get_tf_idf(utterance) for utterance in self.utterances]

    def _compute_doc_frequencies(self):
        """Compute the document frequencies (necessary for IDF)"""

        doc_freqs = {}
        for utterance in self.utterances:
            for word in set(utterance):
                doc_freqs[word] = doc_freqs.get(word, 0) + 1
        return doc_freqs

    def get_tf_idf(self, utterance):
        """Compute the TF-IDF vector of an utterance. The vector can be represented
        as a dictionary mapping words to TF-IDF scores."""

        tf_idf_vals = {}
        word_counts = {word: utterance.count(word) for word in utterance}
        for word, count in word_counts.items():
            idf = math.log(len(self.utterances) / (self.doc_freqs.get(word, 0) + 1))
            print("word", word, count)
            tf_idf_vals[word] = count * idf
        return tf_idf_vals

    def _get_norm(self, tf_idf):
        """Compute the vector norm"""

        return math.sqrt(sum([v**2 for v in tf_idf.values()]))

    def get_response(self, query):
        """
        Finds out the utterance in the corpus that is closed to the query
        (based on cosine similarity with TF-IDF vectors) and returns the
        utterance following it
        """

        if isinstance(query, str):
            query = query.lower().strip().split()

        tf_idf_query = self.get_tf_idf(query)
        cosines = np.zeros(len(self.utterances))
        for i in range(len(cosines)):
            if set(self.utterances[i]) & set(query):
                cosines[i] = self._compute_cosine(tf_idf_query, self.tf_idfs[i])

        most_similar = np.argmax(cosines)
        print("most similar", self.utterances[most_similar])

        if most_similar < len(self.utterances) - 1:
            return " ".join(self.utterances[most_similar + 1])

    def _compute_cosine(self, tf_idf1, tf_idf2):
        """Computes the cosine similarity between two vectors"""

        dotproduct = 0
        for word, tf_idf_val in tf_idf1.items():
            if word in tf_idf2:
                dotproduct += tf_idf_val * tf_idf2[word]

        return dotproduct / (self._get_norm(tf_idf1) * self._get_norm(tf_idf2))


if __name__ == "__main__":
    cb = Chatbot("lotr.en")
    cb.get_response("hello.")
