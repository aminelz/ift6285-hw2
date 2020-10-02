"""
Handles the io of the correction program
"""
import argparse
from argparse import Namespace
from sys import stdin
from typing import Dict, Iterator
import time

parsed_args: Namespace

class Timer:
    __instance = None
    is_timing = False

    @staticmethod
    def get_current_timer():
        """
        Get a singleton instance of the timer
        """
        if Timer.__instance is None:
            raise Exception("No timer")
        return Timer.__instance

    def __init__(self, path: str):
        """Creates a timer instance

        Args:
            path (str): Path to the file where to put the time
        """
        self.start = time.time()
        self.path_to_log = path

        # clean up the log file
        open(self.path_to_log, 'w').close()

        Timer.is_timing = True
        Timer.__instance = self

    def log(self):
        """
        Logs the elapsed time since instantiation
        """
        with open(self.path_to_log, 'a') as time_log:
            time_log.write("{}\n".format(time.time() - self.start))


def get_args() -> Dict[str, str]:
    """Gathers command line arguments and prepares output file if needed

    Returns:
        Dict[str, str]: Argument values, keys: [vocabulary, input_file, output_file]
    """
    parser = argparse.ArgumentParser(
        description="Corrects a list of misspelled words, using Levenshtein by default.")

    parser.add_argument('vocabulary', type=str,
                        help="Vocabulary related to the list of misspellings")

    parser.add_argument('--input', dest='input_file',
                        help="Input file of misspellings. By default, the program reads from stdin.")

    parser.add_argument('--output', dest='output_file',
                        help="Output file of the suggested corrections. By default, it is stdin.")

    parser.add_argument('--time', dest='is_timing', action='store_const', const=True,
                        default=False,
                        help="Whether to time the execution of the script into a file called time_name-of-distance.csv")

    # choose one distance model
    distance_choices = parser.add_mutually_exclusive_group()

    distance_choices.add_argument('--levenshtein', dest='distance', action='store_const',
                                  const='levenshtein',
                                  help="Uses the Levenshtein distance implementation from pyspellchecker")

    distance_choices.add_argument('--levenshtein2', dest='distance', action='store_const',
                                  const='levenshtein2',
                                  help="Uses the Levenshtein distance implementation from Levenshtein")

    distance_choices.add_argument('--hamming', dest='distance', action='store_const',
                                  const='hamming',
                                  help="Uses the Hamming distance")

    distance_choices.add_argument('--jarowinkler', dest='distance', action='store_const',
                                  const='jarowinkler',
                                  help="Uses the Jaro-Winkler distance")

    # parse the args
    args = parser.parse_args()

    arg_dict = {"vocabulary": args.vocabulary, "input_file": args.input_file,
                "distance": args.distance if args.distance is not None else "levenshtein"}

    # output file is emptied
    if args.output_file is not None:
        open(args.output_file, 'w').close()
    global parsed_args
    parsed_args = args

    # start timer if needed
    if args.is_timing:
        _ = Timer("time_{}.csv".format(arg_dict['distance']))

    return arg_dict


def get_misspelling() -> Iterator[str]:
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
                yield line.strip()


def output(message: str):
    """Prints to the stdout or appends to the end of the given file.
    Logs the time, if enabled in the command line.

    Args:
        message (str): String to output
    """
    if parsed_args.output_file is None:
        print(message)
    else:
        with open(parsed_args.output_file, 'a+') as out:
            out.write(message + "\n")
    
    # time
    if Timer.is_timing:
        timer = Timer.get_current_timer()
        timer.log()
