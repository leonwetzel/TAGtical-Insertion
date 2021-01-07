#!/usr/bin/env python3
import pytest

from tagtical_insertion.preprocessing.extraction import get_coordinates


class TestClassExtraction:

    def test_get_coordinates(self):
        """

        Returns
        -------

        """
        sentence = "The door is opening now ."
        tokens = ['The', 'door', 'is', 'opening', 'now', '.']
        tags = ['DEF', 'CON', 'NOW', 'EXG', 'NOW', 'NIL']
        assert get_coordinates(tokens, tags, sentence) ==\
               [(0, 3, 'DEF'), (4, 8, 'CON'), (9, 11, 'NOW'),
                (12, 19, 'EXG'), (20, 23, 'NOW'), (24, 25, 'NIL')]


if __name__ == '__main__':
    pytest.main()
