import unittest
import codecs

from the_gannet import parse_my_clippings


class TestBasicParsing(unittest.TestCase):
    def setUp(self):
        test_file = 'tests/fixtures/basic-My-Clippings-tests.txt'
        with codecs.open(test_file, 'r', 'utf-8') as clips:
            self.found = parse_my_clippings(clips)

    @unittest.skip('not yet')
    def test_not_yet(self):
        expected = True
        actual = False
        self.assertEqual(expected, actual)

    def test_basic(self):
        expected = 'their products,'
        actual = self.found[0]['content']
        self.assertEqual(expected, actual)

    # "Start with Why"
    def test_basic_record(self):
        record = self.found[0]
        expected_title = ('Start with Why: '
                          'How Great Leaders Inspire Everyone to Take Action')
        expected_date = '2012-05-08T18:46:10.000Z'
        self.assertEqual(expected_title, record['title'])
        self.assertEqual('Highlight', record['record_type'])
        self.assertEqual('631', record['location'][0])
        self.assertEqual('Sinek, Simon', record['authors'][0])
        self.assertEqual('43', record['page'][0])
        self.assertEqual(expected_date, record['date'])

    # "The Cluetrain Manifesto"
    def test_multiple_authors(self):
        record = self.found[1]
        self.assertEqual(5, len(record['authors']))

    # "Neuromancer"
    def test_unnumbered_page(self):
        record = self.found[2]
        self.assertEqual('Unnumbered', record['page'][0])

    # "The Art of Doing Science and Engineering"
    # "Constellation Games"
    def test_bookmark_and_note_record_types(self):
        self.assertEqual('Bookmark', self.found[3]['record_type'])
        self.assertEqual('Note', self.found[4]['record_type'])

    # "Constellation Games"
    def test_has_location_but_not_page(self):
        record = self.found[4]
        self.assertEqual('2545', record['location'][0])
        self.assertNotIn('page', record)

    # "Coleman-Coding-Freedom"
    # test_has_no_author

    # "The Last Command"
    def test_title_has_multiple_parentheses(self):
        record = self.found[5]
        expected = ('The Last Command: '
                    'Star Wars (The Thrawn Trilogy): '
                    'Volume 3 (Star Wars: The Thrawn Trilogy)')
        self.assertEqual(expected, record['title'])
        self.assertEqual('Zahn, Timothy', record['authors'][0])

    # "Orthodoxy"
    @unittest.skip("We can't handle these types of records yet.")
    def test_can_handle_timezone_in_date_field(self):
        pass
