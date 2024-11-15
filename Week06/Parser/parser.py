import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S
NP -> N | Det N | Det Adj N | Adj NP | P NP | NP P NP
VP -> V | V NP | V PP | VP Conj VP | VP Adv | Adv VP
PP -> P NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)

def main():
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()
    else:
        s = input("Sentence: ")

    s = preprocess(s)
    trees = list(parser.parse(s))
    if not trees:
        return

    for tree in trees:
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))

def preprocess(sentence):
    sentence = sentence.lower()
    words = nltk.word_tokenize(sentence)
    return [word for word in words if any(char.isalpha() for char in word)]

def np_chunk(tree):
    result = []
    for sub in tree.subtrees():
        if sub.label() == "NP" and not any(child.label() == "NP" for child in sub.subtrees(lambda t: t != sub)):
            result.append(sub)
    return result

if __name__ == "__main__":
    main()
