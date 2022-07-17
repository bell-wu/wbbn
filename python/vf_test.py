import unittest
import verse_finder as vf

class TestVerseFinder(unittest.TestCase):

    def test_basic(self):
        expected = "Rev. 17:14 - These will make war with the Lamb, and the Lamb will overcome them, for He is Lord of lords and King of kings; and they who are with Him, the called and chosen and faithful, will also overcome them."
        actual = vf.find_verses("rev.17:14")[0]
        self.assertEqual(expected, actual)

    def test_basic_2(self):
        expected = "Psa. 110:3 - Your people will offer themselves willingly / In the day of Your warfare, / In the splendor of their consecration. / Your young men will be to You / Like the dew from the womb of the dawn."
        actual = vf.find_verses("psa110:3")[0]
        self.assertEqual(expected, actual)

    def test_ref_with_space(self):
        expected = "Gen. 1:1 - In the beginning God created the heavens and the earth."
        actual = vf.find_verses("gen 1: 1")[0]
        self.assertEqual(expected, actual)

    def test_book_with_number(self):
        expected = "1 Tim. 2:4 - Who desires all men to be saved and to come to the full knowledge of the truth."
        actual = vf.find_verses("1tim. 2:4")[0]
        self.assertEqual(expected, actual)

    def test_book_with_number(self):
        expected = [
            "Mat. 5:5 - Blessed are the meek, for they shall inherit the earth.",
            "Mat. 5:6 - Blessed are those who hunger and thirst for righteousness, for they shall be satisfied.",   
            "Mat. 5:7 - Blessed are the merciful, for they shall be shown mercy.",
            "Mat. 5:8 - Blessed are the pure in heart, for they shall see God.",
            "Mat. 5:9 - Blessed are the peacemakers, for they shall be called the sons of God.", 
            "Mat. 5:10 - Blessed are those who are persecuted for the sake of righteousness, for theirs is the kingdom of the heavens."
        ]
        actual = vf.find_verses("matt.5:5-10")
        self.assertEqual(expected, actual)

    def test_outline_in_between_verse(self):
        expected = "Eph. 3:18 - May be full of strength to apprehend with all the saints what the breadth and length and height and depth are"
        actual = vf.find_verses("eph.3:18")[0]
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()