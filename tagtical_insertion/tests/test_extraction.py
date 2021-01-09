#!/usr/bin/env python3
import pytest

from tagtical_insertion.preprocessing.extraction import get_coordinates


class TestClassExtraction:
    """
    Test suite for functionality concerning extraction of information.
    """
    parameters = [
        ('The door is opening now .',
         ['The', 'door', 'is', 'opening', 'now', '.'],
         ['DEF', 'CON', 'NOW', 'EXG', 'NOW', 'NIL'],
         [(0, 3, 'DEF'), (4, 8, 'CON'), (9, 11, 'NOW'),
          (12, 19, 'EXG'), (20, 23, 'NOW'), (24, 25, 'NIL')]
         ),
        ("I like London and Berlin .",
         ['I', 'like', 'London', 'and', 'Berlin', '.'],
         ['PRO', 'ENS', 'LOC', 'GRP', 'LOC', 'NIL'],
         [(0, 1, 'PRO'), (2, 6, 'ENS'), (7, 13, "LOC"),
          (14, 17, 'GRP'), (18, 24, "LOC"), (25, 26, 'NIL')]
         ),
        ("I 've never been skiing .",
         ["I", "'ve", "never", "been", "skiing", "."],
         ["PRO", "NOW", "NOT", "PFT", "EXG", "NIL"],
         [(0, 1, 'PRO'), (2, 5, 'NOW'), (6, 11, 'NOT'),
          (12, 16, 'PFT'), (17, 23, 'EXG'), (24, 25, 'NIL')]
         ),
        ("Tom joined a political~party .",
         ['Tom', 'joined', 'a', 'political~party', '.'],
         ['PER', 'EPS', 'DIS', 'GRP', 'NIL'],
         [(0, 3, 'PER'), (4, 10, 'EPS'), (11, 12, 'DIS'),
          (13, 28, 'GRP'), (29, 30, 'NIL')]
         ),
        ("Where is Prairie~View~A&M~University ?",
         ['Where', 'is', 'Prairie~View~A&M~University', '?'],
         ['QUE', ''])
    ]

    @pytest.mark.parametrize('sentence, tokens, tags, expected',
                             parameters)
    def test_get_coordinates(self, sentence, tokens, tags, expected):
        """Test the coordination retrieval functionality
        of the function get_coordinates() in the package
        tagtical_insertion.preprocessing.extraction.

        Returns
        -------

        """
        assert get_coordinates(tokens, tags, sentence) == expected

        def test_extract_from_conll(self):
            assert 1 == 1


if __name__ == '__main__':
    pytest.main()
