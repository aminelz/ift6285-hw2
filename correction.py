#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict
from input_output import get_args, get_misspelling, output
import json

# Create dictionary out of the given textfile


def create_dictionary(my_path: str) -> Dict[str, int]:
    """Creates a json dictionary for Levenshtein distance computations

    Args:
        my_path (str): path to the txt vocabulary
    """

    lexique = {}
    json_name = "lexique.json"
    with open(my_path, "r", encoding='utf-8') as txt:
        for line in txt:
            count = line.strip().split(' ', 1)[0]
            word = line.strip().split(' ', 1)[1].replace(u'\xa0', ' ')

            lexique[word] = int(count)
    # ouput the dictionary to a json file
    with open(json_name, "w") as out_json:
        json.dump(lexique, out_json, indent=4)

    return lexique


def main():

    args = get_args()

    # path to the text file of the vocabulary and create a dictionary
    vocabulary_path = args['vocabulary']
    vocabulary = create_dictionary(vocabulary_path)

    # decide which distance to use
    if args['distance'] == 'levenshtein':
        # Levenshtein distance
        from levenshtein import levenshtein_distance
        levenshtein_distance(get_misspelling(), 'lexique.json')
    
    elif args['distance'] == 'levenshtein2':
        # Levenshtein distance using another library
        from levenshtein_v2 import levenshtein_distance2
        levenshtein_distance2(get_misspelling(), vocabulary)
    
    elif args['distance'] == 'hamming':
        # Hamming distance
        from hamming import hamming_distance
        hamming_distance(get_misspelling(), vocabulary)

    elif args['distance'] == 'jarowinkler':
        # Jaro-Winkler
        from jarowinkler import jarowinkler_distance
        jarowinkler_distance(get_misspelling(), vocabulary)
    
    else:
        raise Exception("Unknown distance function : {}".format(args['distance']))
        

if __name__ == "__main__":
    main()
