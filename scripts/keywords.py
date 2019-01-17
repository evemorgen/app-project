__author__ = "Aleksandra Grzeda"

import operator
import sys


def tokenize(book):
    words = book.lower() \
                .replace("\n", "") \
                .replace(".", " ") \
                .replace("*", " ") \
                .replace("(", " ") \
                .replace(")", " ") \
                .replace(",", " ") \
                .split(" ")
    return words


def map_book(tokens):
    hash_map = dict()

    for element in tokens:
        if element in hash_map:
            hash_map[element] += 1
        else:
            hash_map[element] = 1
    return hash_map


file = open(sys.argv[1], 'r')
words = tokenize(file.read())
map = map_book(words)
sorted_x = sorted(map.items(), key=operator.itemgetter(1), reverse=True)

for word, occ in sorted_x:
    print(f'Word: [{word}] Frequency: {occ}')
