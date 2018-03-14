wwf_letters = {
    'a': (1, 9),
    'b': (4, 2),
    'c': (4, 2),
    'd': (2, 5),
    'e': (1, 13),
    'f': (4, 2),
    'g': (3, 3),
    'h': (4, 4),
    'i': (1, 8),
    'j': (10, 1),
    'k': (5, 1),
    'l': (2, 4),
    'm': (4, 2),
    'n': (2, 5),
    'o': (1, 8),
    'p': (4, 2),
    'q': (10, 1),
    'r': (1, 6),
    's': (1, 5),
    't': (1, 7),
    'u': (2, 4),
    'v': (5, 2),
    'w': (4, 2),
    'x': (8, 1),
    'y': (3, 2),
    'z': (10, 1)
}


def word_violates_tilecounts(word):
    counts = {}
    for c in word:
        if c in counts:
            counts[c] += 1
            if counts[c] > wwf_letters[c][1]:
                return True
        else:
            counts[c] = 1
    return False


def compute_word_score(word):
    acc = 0
    for c in word:
        if c in wwf_letters:
            acc += wwf_letters[c][0]
    return acc
