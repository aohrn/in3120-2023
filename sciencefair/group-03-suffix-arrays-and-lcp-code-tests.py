#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from context import in3120


class TestLCPSuffixArray(unittest.TestCase):
    def test_sorting(self):
        with open("../data/names.txt") as file:
            txt = ' '.join(file.readlines())
            engine = in3120.LCPSuffixArray(txt)
            pos = engine.get_sorted_pos()

            for i in range(len(pos) - 1):
                self.assertLessEqual(txt[pos[i]:], txt[pos[i + 1]:])

    def test_evaluation(self):
        with open("../data/names.txt") as file:
            txt = ' '.join(file.readlines())
            engine = in3120.LCPSuffixArray(txt)
            test_list = [
                ("Ashley", 42),
                ("rown", 73),
                ("Lisa", 41),
                ("Keith", 8),
                ("xxx", 0)
            ]

            for word, total_matches in test_list:
                results_number = 0

                positions = engine.evaluate(word)
                for start, end in positions:
                    results_number += 1
                    self.assertEqual(word, txt[start:end])

                self.assertEqual(results_number, total_matches)

