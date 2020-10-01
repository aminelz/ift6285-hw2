#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict, Iterator
from input_output import get_args, get_misspelling, output
from spellchecker import SpellChecker  
import json



#Create dictionary out of the given textfile
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
    #ouput the dictionary to a json file
    with open(json_name,"w") as out_json:
        json.dump(lexique, out_json, indent=4)

    return lexique

def levenshtein_distance(words: Iterator[str]):
    """Corrects the words based on Levenshtein distances

    Args:
        words (Iterator[str]): Iterator over the misspelled words
    """

    # Create instance of spellchecker
    spell = SpellChecker()
    
    # Load out custom made dictionary
    spell.word_frequency.load_dictionary("./lexique.json")

    for word in words:
        suggestions = sorted(spell.candidates(word), key=spell.word_probability)

        output("{misspelled}\t{corrections}".format(\
            misspelled=word, \
                corrections= "\t".join(suggestions[:5])
            )) # may cause IO bottleneck

def main():

    args = get_args()

    # path to the text file of the vocabulary and create a dictionary
    vocabulary_path = args['vocabulary']
    vocabulary = create_dictionary(vocabulary_path)

    # Levenshtein distance
    levenshtein_distance(get_misspelling())

if __name__ == "__main__":
    main()



# with open("./devoir3-train.txt", "r") as dataset:
#     lines = np.zeros(len(f.readlines()), )
#     for i in range(len(f.readlines())):
        
#         print(line)


# Lexique = "mon lexique et sa frequence"
# Mots = "mes mots"
# Corrections = "mes corrections"

# for (i, mot) in enumerate(Mots):

#     distances = np.zeros((len(Lexique), 2))

#     for (j, lex) in enumerate(lexique):
#         distances[j,0] = dist_func(mot, lex)
#         distances[j,1] = j 
    
#     np.sort(distances, )
