from typing import Iterator
from spellchecker import SpellChecker
from input_output import output


def levenshtein_distance(words: Iterator[str], vocabulary: str):
    """Corrects the words based on Levenshtein distances

    Args:
        words (Iterator[str]): Iterator over the misspelled words
        vocabulary (str) : Path to the json file holding the vocabulary
    """

    # Create instance of spellchecker
    spell = SpellChecker()

    # Load out custom made dictionary
    spell.word_frequency.load_dictionary(vocabulary)

    for word in words:
        suggestions = sorted(spell.candidates(
            word), key=spell.word_probability)

        output("{misspelled}\t{corrections}".format(
            misspelled=word,
            corrections="\t".join(suggestions[:5])
        ))  # may cause IO bottleneck
