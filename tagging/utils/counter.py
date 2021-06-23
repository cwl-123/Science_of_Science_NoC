import re


def count_word(dst, src):
    return len(re.findall(f'\\b{dst}\\b', str(src), re.IGNORECASE))


def count_tab(src):
    return len(re.findall(r'\t', str(src)))
