import nltk
from nltk import word_tokenize, pos_tag
import string


def get_phrase(sentences: list):
    phrase = []
    grammar = r'NBAR: {<NN.*|JJ.*>*<NN.*>}'
    pattern = nltk.RegexpParser(grammar)
    for idx, text in enumerate(sentences):
        tokens = word_tokenize(text)
        tags = pos_tag(tokens)
        tree = pattern.parse(tags)
        for subtree in tree.subtrees():
            if subtree.label() in ['NBAR']:
                kw = ' '.join(map(lambda t: t[0], subtree.leaves()))
                phrase.append(kw)
    phrase = filter(lambda p: not fail_rules_check(p), phrase)
    return list(set(phrase))


def fail_rules_check(phrase):
    """
    fail_rules_check - 过滤不合要求的词

    Args:
      phrase - Unicode
    Returns:
      True  - 触发规则需要过滤
      False - 正常词
    """
    numset = frozenset("0123456789.+-")
    puncset = frozenset(string.punctuation)
    assert(isinstance(phrase, str))
    if len(phrase) == 0:
        return True
    # 关键字不包含 "[] 和 %"
    if any([x == "[" or x == "]" or x == "%" for x in phrase]):
        return True
    # 关键字不能是纯数字
    if all([ x in numset for x in phrase]):
        return True
    # 关键字不能纯符号
    if all([ x in puncset for x in phrase]):
        return True
    return False
