from collections import defaultdict
from Lexeme import Lexeme

def load_lexicon(filename):
    # todo add check for comments in txtfiles, will start with'#'
    lexicon = defaultdict(lambda: [])  # maps POS to the Lexemes
    vocab = []  # holds all lexemes
    with open(filename) as f:
        for line in f:
            line = line.split()
            word = line[0]
            POS = line[1]
            features = line[2:]
            feature_dictionary = defaultdict(lambda: [])
            for feature in features:
                feat = feature.split(':')
                feat_type = feat[0]
                feat_val = feat[1]
                # build the feature dictionary
                feature_dictionary[feat_type].append(feat_val)
            lexeme = Lexeme(word=word,
                            POS=POS,
                            features=feature_dictionary
                            )
            vocab.append(lexeme)
            lexicon[POS].append(lexeme)
    return lexicon, vocab


def load_templates(filename):
    with open(filename) as f:
        templates=[]
        for line in f:
            templates.append(line.split())
    return templates

def load_grammar(filename):
    grammar = defaultdict(list)
    with open(filename) as f:
        for line in f:
            line = line.split()
            lhs = line[0].split("-")
            nonterminal = lhs[0]
            lhs_features = lhs[1:]
            productions = [production.split("-") for production in line[2:]]
            grammar[nonterminal].append((productions,lhs_features))
    return grammar


class GrammarChecker():

    def __init__(self):
        # lexicon maps POS to list of Lexemes with that POS, vocab is list of all lexemes
        self.lexicon, self.vocab = load_lexicon(filename='lexicon.txt')
        self.templates = load_templates(filename='templates.txt')  # list of lists of possible sentences
        self.grammar = load_grammar(filename='grammar.txt')  # dict of POS to rewrite rule
        # self.vocab = [word[0] for word in self.lexicon[symbol]]

    def check_grammar(self, sentence):
        sentence = sentence.split()
        return self.recursive_parse(sentence, "S", 0)

    def recursive_parse(self, sentence, symbol, index, debug=False):
        if debug: print(symbol, index)

        # base case: we have a terminal node, e.g. NNP > Elaine
        if symbol in self.lexicon:  # if this is a POS, terminal node, no rewrite rule
            possible_words = set( [lexeme.word for lexeme in self.lexicon[symbol]] )
            if index >= len(sentence):
                return "YIKES"
            word = sentence[index]
            if word in possible_words:
                return ([symbol], index + 1)
            else:
                return "YIKES: Word is not in lexicon: %s" % word

        ## recursive case: we have a rewrite rule
        tree = [symbol]
        productions = self.grammar[symbol]
        productions = [production[0] for production in productions]
        for rule in productions:
            tempindex = index
            tempchildren = []
            failure = False
            for element in rule:
                return_value = self.recursive_parse(sentence, element[0], tempindex)
                if type(return_value) == str: # "YIKES" occured
                    failure = True
                    break
                else:
                    subtree, tempindex = return_value
                    tempchildren.append(subtree)

            if not failure:
                tree.extend(tempchildren)
                return (tree, tempindex)
        return "YIKES"

    def is_grammatical(self, sentence):
        return type(self.check_grammar(sentence))


if __name__ == '__main__':
    sentence = "Elaine admired a platypus"
    gc = GrammarChecker()
    tree = gc.check_grammar(sentence)
