####
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
        raise NotImplementedError()

    def _compute_doc_frequencies(self):
        """Compute the document frequencies (necessary for IDF)"""
        raise NotImplementedError()

    def get_tf_idf(self, utterance):
        """Compute the TF-IDF vector of an utterance. The vector can be represented
        as a dictionary mapping words to TF-IDF scores."""
        raise NotImplementedError()

    def get_response(self, query):
        """
        Finds out the utterance in the corpus that is closed to the query
        (based on cosine similarity with TF-IDF vectors) and returns the
        utterance following it.
        """

        # If the query is a string, we first tokenise it
        if type(query) == str:
            query = self._tokenise(query)

        # Your implementation should use the get_tf_idf and compute_cosine
        # methods that are already provided (as well as the TF-IDF values
        # from each utterance in the corpus, stored in self.tf_idfs)
        raise NotImplementedError()

    def compute_cosine(self, tf_idf1, tf_idf2):
        """Computes the cosine similarity between two vectors"""
        raise NotImplementedError()

    def _get_norm(self, tf_idf):
        """Compute the vector norm"""
        raise NotImplementedError()


if __name__ == "__main__":
    TEST_SENTS = [
        "hello world",
        "hello",
        "world",
        "hello world",
        "Who are you?",
        "I am a chatbot",
        "What is the meaning of stonehenge?",
    ]
    cb = Chatbot("lotr.en")
    cb.get_response("hello.")

    for sent in TEST_SENTS:
        print(f"{sent}: {cb.get_response(sent)}")
