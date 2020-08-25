import typing as t


def load_wordlist() -> t.Set[str]:
    with open("words", "r") as f:
        return set(word.strip() for word in f)
