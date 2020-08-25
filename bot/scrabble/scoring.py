import typing as t
import re
import string

_letter_scores = {
    "a": 1,
    "b": 3,
    "c": 3,
    "d": 2,
    "e": 1,
    "f": 4,
    "g": 2,
    "h": 4,
    "i": 1,
    "j": 8,
    "k": 5,
    "l": 1,
    "m": 3,
    "n": 1,
    "o": 1,
    "p": 3,
    "q": 10,
    "r": 1,
    "s": 1,
    "t": 1,
    "u": 1,
    "v": 4,
    "w": 4,
    "x": 8,
    "y": 4,
    "z": 10,
}


def score(word: str) -> int:
    return sum(_letter_scores.get(c, 0) for c in word)


def score_phrase(phrase: str, *, wordlist: t.Set[str]) -> int:
    phrase = phrase.translate(str.maketrans("", "", string.punctuation)).lower()
    words = set(word for word in phrase.split() if len(word) > 1 and word in wordlist)
    print(f"Found {len(words)} valid words in phrase: {words}")
    return sum(score(word) for word in words)
