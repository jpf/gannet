import unittest
import codecs

from gannet import parse_my_clippings


class TestBasicParsing(unittest.TestCase):
    def record_with_title(self, title):
        for record in self.found:
            if title in record['title']:
                return record

    def setUp(self):
        test_file = 'tests/fixtures/basic-My-Clippings-tests.txt'
        with codecs.open(test_file, 'r', 'utf-8') as clips:
            self.found = parse_my_clippings(clips)

    def test_basic(self):
        record = self.record_with_title('Start with Why')
        expected = 'their products,'
        actual = record['highlight']
        self.assertEqual(expected, actual)

    # "Start with Why"
    def test_basic_record(self):
        record = self.record_with_title('Start with Why')
        expected_title = ('Start with Why: '
                          'How Great Leaders Inspire Everyone to Take Action')
        expected_date = '2012-05-08T18:46:10.000Z'
        self.assertEqual(expected_title, record['title'])
        self.assertEqual('Highlight', record['type'])
        self.assertEqual('631', record['locations'][0])
        self.assertEqual('Simon Sinek', record['authors'][0])
        self.assertEqual('43', record['pages'][0])
        self.assertEqual(expected_date, record['date'])

    def test_multiple_authors(self):
        record = self.record_with_title('The Cluetrain Manifesto')
        print record
        self.assertEqual(5, len(record['authors']))

    def test_unnumbered_pages(self):
        record = self.record_with_title('Neuromancer')
        self.assertEqual('Unnumbered', record['pages'][0])

    def test_bookmark_and_note_record_types(self):
        record = self.record_with_title('The Art of Doing Science')
        self.assertEqual('Bookmark', record['type'])
        record = self.record_with_title('Constellation Locations')
        self.assertEqual('Highlight', record['type'])

    def test_has_locations_but_not_pages(self):
        record = self.record_with_title('Constellation Locations')
        self.assertEqual('178', record['locations'][0])
        self.assertNotIn('pages', record)

    def test_has_locations_sort(self):
        record = self.record_with_title('Constellation LocSortTest')
        self.assertEqual('2544', record['locations'][0])
        self.assertEqual('2545', record['locations'][1])

    # "Coleman-Coding-Freedom"
    # test_has_no_author

    def test_note_included_into_highlight(self):
        record = self.record_with_title('Constellation Games')
        print "RECORD:" + str(record)
        self.assertEqual('did $1 apps really do that?', record['note'])
        self.assertIn('highlight', record)

    # "The Last Command"
    def test_title_has_multiple_parentheses(self):
        record = self.record_with_title('The Last Command')
        expected = ('The Last Command: '
                    'Star Wars (The Thrawn Trilogy): '
                    'Volume 3 (Star Wars: The Thrawn Trilogy)')
        self.assertEqual(expected, record['title'])
        self.assertEqual('Timothy Zahn', record['authors'][0])

    # "Orthodoxy"
    @unittest.skip("We can't handle these types of records yet.")
    def test_can_handle_timezone_in_date_field(self):
        pass

    def test_locations_numbers_cleanup(self):
        record = self.record_with_title('Neuromancer')
        expected = ["4195"]
        actual = record['locations']
        self.assertEqual(expected, actual)
