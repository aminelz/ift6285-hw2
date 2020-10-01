#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from spellchecker import SpellChecker  
import json
import sys

#arrays to hold our correct and incorrect words
incorrect_words = []
correct_words = []

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




def main():

    path = "./" +str(sys.argv[1])#"./1voc-1bwc.txt"
    path2 = "./" +str(sys.argv[2]) #"./devoir3-train.txt"

    d = 2

    create_dictionary(path)
    #Create instance of spellchecker
    spell = SpellChecker(language=None, distance=d)
    #Load out custom made disctionary
    spell.word_frequency.load_dictionary("./lexique.json")


    #Create our to be corrected list of words
    with open(path2) as txt2:
        for line in txt2:
            false = line.strip().split("\t", 1)[0]
            correct = line.strip().split("\t", 1)[1].replace(u'\xa0', ' ')
            incorrect_words.append(false)
            correct_words.append(correct)

    output_lines = ""
    for (i, word) in enumerate(incorrect_words):
        candidates = spell.candidates(word)
        to_print = str(word) + "\t"
        local_count = 0
        for cor in candidates:
            if local_count <5:
                to_print += cor + "\t"
                local_count+= 1
            else:
                break
        # print(to_print)
        output_lines += to_print + "\n"

    print(output_lines)
    return output_lines

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
