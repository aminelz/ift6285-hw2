"""
    Checks how well the suggestions are by comparing
    whether the correct answer is in the list of suggestions.

    If the correct answer is the first suggestion, then a full
    score of 1 is given to this word.

    If the correct answer is after the first suggestion, then
    a score of 0.5 is given to this word.

    Otherwise, a score of 0 is given.

    Scoreboard looks like this:
        Total score: 6043/12020
        First suggestion: 3000/12020
        Following suggestion: 6000/12020
        Wrong answer: 6020
"""
import argparse
from argparse import Namespace
from typing import Iterator, List
import sys


def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluates the list of spelling corrections by comparing with a testing set")

    parser.add_argument('solutions', type=str,
                        help="File of correct answers to check against")

    parser.add_argument('testee', type=str,
                        help="File of attempted answers to evaluate")

    return parser.parse_args()


def read_solutions(path: str) -> Iterator[str]:
    """Returns an iterator over the correct words in order of appearance

    Args:
        path (str): Path to the solution file

    Yields:
        Iterator[str]: Iterator over the correct words
    """
    with open(path, 'r') as solutions:
        for line in solutions:
            yield line.strip().split()[1]


def read_attempted(path: str) -> Iterator[List[str]]:
    """Returns an iterator over the suggested words

    Args:
        path (str): Path to the suggestions file

    Yields:
        Iterator[List[str]]: Iterator of the suggested words
    """
    with open(path, 'r') as attempted:
        for line in attempted:
            _, *suggested = line.strip().split()
            yield suggested


def score(args: Namespace) -> Iterator[float]:
    for (solution, attempt) in \
            zip(read_solutions(args.solutions), read_attempted(args.testee)):
        if solution == attempt[0]:
            yield 1
        elif solution in attempt:
            yield 0.5
        else:
            yield 0


def main():

    args = parse()

    scores = {"first": 0, "following": 0, "wrong": 0}

    total_evaluated = 0
    total_score = 0
    for s in score(args):
        total_evaluated += 1
        if s == 1:
            scores['first'] += 1
        elif s == 0.5:
            scores['following'] += 1
        elif s == 0:
            scores['wrong'] += 1
        else:
            print("Unexpected score of {}".format(s), file=sys.stderr)
        total_score += s

    print("""
    Total score: {tally}/{total}
    First suggestion: {first}/{total}
    Following suggestion: {following}/{total}
    Wrong answers: {wrong}/{total}
    """.format(tally=total_score,
               total=total_evaluated,
               first=scores['first'],
               following=scores['following'],
               wrong=scores['wrong']))


if __name__ == "__main__":
    main()
