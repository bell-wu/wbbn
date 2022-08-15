#!/bin/bash

function verse_finder() {
	verse=$(python3 ~/projects/BibleNotes/python/verse_finder.py $1)
	echo -n $verse | pbcopy
	echo $verse
}
