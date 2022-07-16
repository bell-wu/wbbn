import json
import re
import sys

books_of_the_bible = ['1chronicles', '1corinthians', '1john', '1kings', '1peter', '1samuel', '1thessalonians', '1timothy', '2chronicles', '2corinthians', '2john', '2kings', '2peter', '2samuel', '2thessalonians', '2timothy', '3john', 'acts', 'amos', 'colossians', 'daniel', 'deuteronomy', 'ecclesiastes', 'ephesians', 'esther', 'exodus', 'ezekiel', 'ezra', 'galatians', 'genesis', 'habakkuk', 'haggai', 'hebrews', 'hosea', 'isaiah', 'james', 'jeremiah', 'job', 'joel', 'john', 'jonah', 'joshua', 'jude', 'judges', 'lamentations', 'leviticus', 'luke', 'malachi', 'mark', 'matthew', 'micah', 'nahum', 'nehemiah', 'numbers', 'obadiah', 'philemon', 'philippians', 'proverbs', 'psalms', 'revelation', 'romans', 'ruth', 'song of songs', 'titus', 'zechariah', 'zephaniah']
books_with_one_chapter = ['2john', '3john', 'jude', 'obadiah']

class Verse:
    def __init__(self, book, chapter, verse_number):
        self.book = book
        self.chapter = chapter
        self.verse_number = verse_number


def find_verses(references):
    verse_references = references.split(";")

    with open("books.json") as json_file:
        books_with_abbrv = json.load(json_file)
    
    with open("verses.json") as json_file:
        bible = json.load(json_file)
        
        for ref in verse_references:
            v = process_reference(ref)

            if v.book in books_with_one_chapter:
                print(v.book)
                print(v.verse_number)
                verse_text = bible[v.book][v.verse_number]
                verse_reference = books_with_abbrv[v.book] + " " + v.verse_number
            else:
                verse_text = bible[v.book][v.chapter][v.verse_number]
                verse_reference = books_with_abbrv[v.book] + " " + v.chapter + ":" + v.verse_number

            print(verse_reference + " - " + verse_text)


def process_reference(ref):
    # remove punctuation, except :
    ref = re.sub(r"[^a-z0-9:]+", '', ref.lower())

    numbers = re.findall(r"\d+", ref)
    letters = re.findall(r"[a-z]+", ref.split(":")[0])[0]

    # for books that start with a number
    # if len(numbers) == 3:
    if ref.index(numbers[0]) < ref.index(letters):
        letters = numbers[0] + letters
        numbers = numbers[1:]
    book = find_book(letters)

    if book in books_with_one_chapter:
        return Verse(book, "", numbers[-1])
    else:
        return Verse(book, numbers[0], numbers[1])


def find_book(book):
    # ex. if book = "zep", regex_book = "z[a-z]*e[a-z]*p[a-z]*", not sure if this is the best way
    # jk it's too hard to make this work
    # regex_book = "^[" + book[:2] + "]" + "".join(map(lambda x: x + "[a-z]*", book[1:])) if book[0].isdigit() else "^" + "".join(map(lambda x: x + "[a-z]*", book))

    for b in books_of_the_bible:
        # if re.search(regex_book, b):
        if b.startswith(book):
            return b


def main(args):
    find_verses(args[1])

if __name__ == "__main__":
    main(sys.argv)
