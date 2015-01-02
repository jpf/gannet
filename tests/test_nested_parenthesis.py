import unittest
import codecs

from gannet import parse_my_clippings


class TestBasicParsing(unittest.TestCase):
    def record_with_title(self, title):
        for record in self.found:
            if title in record['title']:
                return record

    def setUp(self):
        test_file = 'tests/fixtures/nested-parenthesis-in-author-area.txt'
        with codecs.open(test_file, 'r', 'utf-8') as clips:
            self.found = parse_my_clippings(clips)

    # "Orthodoxy"
    # I'm actually not sure how to handle records with parenthesis
    # in the author area, since I use "QuotedString" to handle this in
    # Pyparsing
    @unittest.skip("We can't handle these types of records yet.")
    def test_can_handle_parenthesis_in_author_field(self):
        record = self.record_with_title('Orthodoxy')
        expected = 'testing'
        self.assertEqual(expected, record['authors'][0])
