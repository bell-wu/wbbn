import json
import re
import sys
from enum import Enum
from html.parser import HTMLParser

"""
Bible Parser

Given an html file of the entire bible, write a map of book -> chapter -> verse as a json file.
ex. python bible_parser.py bible.html verses.json

TODO: add error handling

"""

class ParserState(Enum):
	INITIAL = 0
	FOUND_VERSE_REFERENCE = 1
	FOUND_VERSE_DATA = 2
	FOUND_SUPERSCRIPT = 3

	FOUND_CHAPTER_DATA = 4
	FOUND_VERSE_LINKS = 5
	FOUND_OUTLINE = 6
	FOUND_VERSE_BLOB = 7
	FOUND_POSSIBLE_VERSE_BLOB = 8
	FOUND_PREVNEXT = 9

	FOUND_POSSIBLE_NEW_CHAPTER = 10
	FOUND_INFO = 11 # skip top outlines

	FOUND_NEW_BOOK = 12

class BibleParser(HTMLParser):
	def __init__(self):
		self.bible = {}
		self.verse_number = 0
		self.chapter_title = ""
		self.book_title = ""
		self.state = ParserState.INITIAL
		HTMLParser.__init__(self)

	def handle_starttag(self, tag, attrs):
		# print("Encountered a start tag: ", tag)
		# if len(attrs) > 0:
		# 	print("Encountered attrs: ", attrs)

		if tag == 'p':
			if ('class', 'text-outline') in attrs:
				self.state = ParserState.FOUND_OUTLINE
			if ('class', 'info') in attrs:
				self.state = ParserState.FOUND_INFO
			elif ('class', 'verse-links2') in attrs:
				self.state = ParserState.FOUND_VERSE_LINKS
			elif ('class', 'verse') in attrs:
				# self.state = ParserState.FOUND_VERSE_BLOB
				# self.verse_number += 1
				self.state = ParserState.FOUND_POSSIBLE_VERSE_BLOB
			elif ('class', 'prevnext') in attrs:
				self.state = ParserState.FOUND_PREVNEXT

		if tag == 'a':
			if ('class', 'calibre16') in attrs:
				self.state = ParserState.FOUND_POSSIBLE_NEW_CHAPTER

		if tag == 'b':
			if ('class', 'calibre17') in attrs:
				self.state = ParserState.FOUND_NEW_BOOK
				self.book_title = ""
			elif ('class', 'calibre6') in attrs and self.state == ParserState.FOUND_POSSIBLE_VERSE_BLOB:
				self.state = ParserState.FOUND_VERSE_BLOB
				self.verse_number += 1

		if tag == 'sup' and self.state not in [ParserState.FOUND_OUTLINE, ParserState.FOUND_INFO]:
			self.state = ParserState.FOUND_SUPERSCRIPT

	def handle_data(self, data):
		# print("Encountered some data: ", data)

		if self.state == ParserState.FOUND_VERSE_DATA:
			verse_num = str(self.verse_number)
			if verse_num in self.bible[self.book_title][self.chapter_title]:
				self.bible[self.book_title][self.chapter_title][verse_num] += data
			else:
				self.bible[self.book_title][self.chapter_title][verse_num] = data
		elif self.state == ParserState.FOUND_POSSIBLE_NEW_CHAPTER:
			self.state = ParserState.FOUND_CHAPTER_DATA
			self.chapter_title = data
			self.bible[self.book_title][self.chapter_title] = {}
			self.verse_number = 0
		elif self.state == ParserState.FOUND_NEW_BOOK:
			self.book_title += data
		
	def handle_endtag(self, tag):
		# print("Encountered an end tag: ", tag)

		# found end of verse reference, begin verse data
		if tag == 'b':
			if self.state == ParserState.FOUND_VERSE_BLOB:
				self.state = ParserState.FOUND_VERSE_DATA
			elif self.state == ParserState.FOUND_NEW_BOOK:
				# for books of 1&2 Samuel, 1&2 Chronicles, 1&2 Kings, which share outlines, 
				# I combined the b tags into one for convenience
				# <a href="#calibre_link-1093" class="calibre16"><b class="calibre17">1&nbsp;Chronicles</b></a> &amp; <a href="#calibre_link-1094" class="calibre16"><b class="calibre17">2&nbsp;Chronicles</b></a><b class="calibre17"> Outline</b>
				# <b class="calibre17">1&nbsp;Chronicles &amp; 2&nbsp;Chronicles Outline</b></p>
				self.book_title = self.book_title.replace(" Outline", "") # should prob move this to clean_up_map
				self.state = ParserState.INITIAL
				self.bible[self.book_title] = {}
		
		# # found end footnote tag, going back to verse data
		if tag == 'sup' and self.state == ParserState.FOUND_SUPERSCRIPT: 
			self.state = ParserState.FOUND_VERSE_DATA

		if tag == 'div': 
			self.state = ParserState.INITIAL

		if tag == 'p' and self.state == ParserState.FOUND_OUTLINE:
			self.state = ParserState.FOUND_VERSE_DATA

	def get_bible(self):
		return self.bible

class DummyParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)

	def handle_starttag(self, tag, attrs):
		print("Encountered a start tag:", tag)
		if len(attrs) > 0:
			print("Encountered attrs:", attrs)

	def handle_endtag(self, tag):
		print("Encountered an end tag :", tag)

	def handle_data(self, data):
		print("Encountered some data  :", data)

def extract_bible(filename, result):
	parser = BibleParser()
	# parser = DummyParser()

	f = open(filename, "r")
	for line in f:
		if line: 
			parser.feed(line)

	b = clean_up_map(parser.get_bible())
	# smart_print_map(b)

	with open(result, 'w') as fp:
		json.dump(b, fp)

	f.close()

def clean_up_map(m):
	n = {}
	for k in m.keys():
		new_key = k.lower() # lowercase book names for convenience

		split_books = new_key.split("  ")
		split_chapter_title = k.split(" ")

		if new_key in ("2john", "3john", "jude", "obadiah"):
			n[new_key] = clean_up_map(m[k][m[k].keys()[0]])
		elif type(m[k]) == dict:
			# clean up book names like "1Samuel  2Samuel" -> "1Samuel", "2Samuel"
			if len(split_books) == 2:
				book1, book2 = split_books
				n[book1] = {}
				n[book2] = {}
				for chapter in m[k].keys():
					if m[k][chapter]:
						p = clean_up_map(m[k][chapter])
						number_only_chapter = chapter.split(" ")[-1]
						if chapter[0] == '1':
							n[book1][number_only_chapter] = p
						else:
							n[book2][number_only_chapter] = p

			# remove book names from chapter "JUDGES 8" -> "8"
			elif len(split_chapter_title) >= 2 and split_chapter_title[-1].isdigit():
				chapter_number = split_chapter_title[-1]
				n[chapter_number] = clean_up_map(m[k])

			# remove empty dicts
			elif m[k]:
				n[new_key] = clean_up_map(m[k])

		# remove extraneous spaces and new lines
		elif new_key != "0": # for removing "0" verses lol
			n[new_key] = re.sub("\s+", " ", m[k]).strip()
	return n


def smart_print_map(m, indent = 0):
	p = sorted(m.keys())
	for k in p:
		print("  " * indent + k)
		if type(m[k]) == dict:
			smart_print_map(m[k], indent + 1)
		else:
			print("  " * (indent + 1) + m[k][:20])


def main(args):
	extract_bible(args[1], args[2])

if __name__ == "__main__":
    main(sys.argv)