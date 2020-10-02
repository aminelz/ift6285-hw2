from typing import Iterator
from input_output import output
from Levenshtein import jaro_winkler
import numpy as np

def jarowinkler_distance(words: Iterator[str], vocabulary: str):
    """Corrects the words based on JaroWinkler distances

    Args:
        words (Iterator[str]): Iterator over the misspelled words
        vocabulary (str) : dictionary holding words and their frequency
    """

    for word in words:
        distances = []
        suggestions = []
        vocab_list = list(vocabulary)
        for (i,vocab) in enumerate(vocab_list):
            distances.append(jaro_winkler(word, vocab))
        idx = np.array(distances).argsort()[::-1][:5]
        
        for i in range(5):
            for j in range(i+1,5):
                if distances[idx[i]] == distances[idx[j]]:
                    if vocabulary.get(vocab_list[idx[i]]) < vocabulary.get(vocab_list[idx[j]]):
                        temp = idx[i] 
                        idx[i] = idx[j]
                        idx[j] = temp   

        for i in idx:
            suggestions.append(vocab_list[i])

        output("{misspelled}\t{corrections}".format(
            misspelled=word,
            corrections="\t".join(suggestions)
        ))  # may cause IO bottleneck
