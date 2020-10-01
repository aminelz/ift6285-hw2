"""
Handles the io of the correction program
"""
import argparse
from argparse import Namespace
from sys import stdin
from typing import Dict, Iterator, Optional

parsed_args: Optional[Namespace] = None

def get_args() -> Dict[str, str]:
    """Gathers command line arguments and prepares output file if needed

    Returns:
        Dict[str, str]: Argument values, keys: [vocabulary, input_file, output_file]
    """
    parser = argparse.ArgumentParser(\
        description="Corrects a list of misspelled words")

    parser.add_argument('vocabulary', type=str, \
        help="Vocubulary related to the list of misspellings")

    parser.add_argument('--input', dest='input_file', \
        help="Input file of misspellings. By default, the program reads from stdin.")

    parser.add_argument('--output', dest='output_file', \
        help="Output file of the suggested corrections. By default, it is stdin.")

    args = parser.parse_args()

    # output file is emptied
    if args.output_file is not None:
        open(args.output_file, 'w').close()
    global parsed_args
    parsed_args = args

    return {"vocabulary": args.vocabulary, "input_file": args.input_file}

def get_misspelling() -> Iterator[str] :
    """Get a misspelled word from stdin or the given file.
    One misspelling per line.

    Yields:
        Iterator[str]: A generator over strings
    """
    if parsed_args.input_file is None:
        for line in stdin:
            yield line.strip()

    else:
        with open(parsed_args.input_file, 'r') as misspellings:
            for line in misspellings:
                yield line

def output(message: str):
    """Prints to the stdout or appends to the end of the given file.

    Args:
        message (str): String to output
    """
    if parsed_args.output_path is None:
        print(message)
    else:
        with open(parsed_args.output_path, 'a+') as out:
            out.write(message + "\n")