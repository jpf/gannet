import unittest
import codecs

from gannet import parse_my_clippings


class TestClippingId(unittest.TestCase):
    def record_with_title(self, title):
        for record in self.found:
            if title in record['title']:
                return record

    def setUp(self):
        test_file = 'tests/fixtures/basic-My-Clippings-tests.txt'
        with codecs.open(test_file, 'r', 'utf-8') as clips:
            self.found = parse_my_clippings(clips)

    def test_clipping_has_id(self):
        clipping = self.record_with_title('Start with Why')
        self.assertIn('cid', clipping)

    def test_clipping_id_matches(self):
        clipping = self.record_with_title('Start with Why')
        self.assertIn('cid', clipping)
        expected = 'ff3fddcce7f27d20c8a37bdae1f1318e651ec2e3'
        actual = clipping['cid']
        self.assertEqual(expected, actual)
