import sys

def spell_check(filename):
    f = open(filename, "rw")
    previous_word = ""
    current_word = ""
    next_word = ""

    for line in f:
        # remove punctuation, maybe not apostrophes
        
        words = line.split(" ")
        for word in words:
            next_word = word

            # check if current_word in dict

            # check previous_word + current_word, if that's in dict

            # check current_word + next_word, if that's in dict


            # shift words
            previous_word = current_word
            current_word = next_word

def main(args):
    print(args[1])


if __name__ == "__main__":
    main(sys.argv)