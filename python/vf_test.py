import unittest
import verse_finder as vf

class TestStringMethods(unittest.TestCase):

    def test_basic(self):
        expected = "These will make war with the Lamb, and the Lamb will overcome them, for He is Lord of lords and King of kings; and they who are with Him, the called and chosen and faithful, will also overcome them."
        actual = vf.find_verses("rev.17:14")
        self.assertEqual(expected, actual)

    def test_ref_with_space(self):
        expected = "In the beginning God created the heavens and the earth."
        actual = vf.find_verses("gen 1: 1")
        self.assertEqual(expected, actual)

    def test_book_with_number(self):
        actual = vf.find_verses("1tim. 2:4")
        pass

    def test_book_with_number(self):
        actual = vf.find_verses("matt.5:5-10")
        pass

    def test_outline_in_between_verse(self):
        expected = "May be full of strength to apprehend with all the saints what the breadth and length and height and depth are"
        actual = vf.find_verses("eph.3:18")
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()