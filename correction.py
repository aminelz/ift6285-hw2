#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from input_output import get_args, get_misspelling, output
import numpy as np
from spellchecker import SpellChecker  
import json
import sys



#Create dictionary out of the given textfile
def create_dictionary(my_path):
    
    lexique = {}
    json_name = "lexique.json"
    with open(my_path, "r") as txt:
        for line in txt:
            count = line.strip().split(' ', 1)[0]
            word = line.strip().split(' ', 1)[1].replace(u'\xa0', ' ')
            
            lexique[word] = int(count)
    #ouput the dictionary to a json file
    with open(json_name,"w") as out_json:
        json.dump(lexique, out_json,ensure_ascii=False, indent=4)

    return lexique

def corrige_Lev(word, spell):
    sttm = ["null","null","null","null","null"]
    candidates = list(spell.candidates(word))
    count = 0
    for (i,can) in enumerate(candidates):
        if count < 5:
            sttm[i] = candidates[i]
            count += 1
        else:
            break
    return sttm

def main():

    args = get_args()

    # path to the text file of the vocabulary
    vocabulary_path = args['vocabulary']

    # path to the text file of misspellings
    misspelling_path = args['input_file']

    # arrays to hold our correct and incorrect words
    incorrect_words = []
    correct_words = []
    ever_predicted = 0
    first_predicted = 0
    edit_distance = 2

    lexique = create_dictionary(vocabulary_path)
    # Create instance of spellchecker
    spell = SpellChecker(language=None, distance=edit_distance)
    # Load out custom made disctionary
    spell.word_frequency.load_dictionary("./lexique.json")

    # Create our to be corrected list of words
    for line in get_misspelling():
        false = line.strip().split("\t", 1)[0]
        correct = line.strip().split("\t", 1)[1].replace(u'\xa0', ' ')
        incorrect_words.append(false)
        correct_words.append(correct)

    output_lines = ""
    for (i, word) in enumerate(incorrect_words):
        candidates_lev = corrige_Lev(word, spell)
        to_print = str(word) + "\t"
        if correct_words[i] in candidates_lev:
            if correct_words[i] == candidates_lev[0]:
                first_predicted += 1
            ever_predicted += 1

        for cand in candidates_lev:
            if cand == "null":
                break
            else:
                to_print += cand + "\t"

        output_lines += to_print + "\n"
    performance = str("Right Corrections found = " + str(ever_predicted) + " = %" + str(round(ever_predicted/len(correct_words)*100, 2)) +
                      "\n" + "Right Correction in first candidate = " + str(first_predicted)+" = %" + str(round(first_predicted/len(correct_words)*100, 2)))
    output_lines += performance

    output(output_lines)

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
