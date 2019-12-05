import re
import sys

from preprocessors.fce.format_fce import tokenize, parse


def generate_typo_pair(tree):
    src = []
    tgt = []
    correct = None
    incorrect = None
    for elem in tree:
        if isinstance(elem, str):
            src += [elem]
            tgt += [elem]
        if isinstance(elem, dict):
            if elem['tag'] == 'i':
                if len(elem['children']) == 1 and isinstance(elem['children'][0], str):
                    incorrect = elem['children'][0]
                else:
                    incorrect = generate_typo_pair(elem['children'])
            elif elem['tag'] == 'c':
                if len(elem['children']) == 1 and isinstance(elem['children'][0], str):
                    correct = elem['children'][0]
                else:
                    correct = generate_typo_pair(elem['children'])
            elif elem['tag'] == 'NS':
                src_sub, tgt_sub = generate_typo_pair(elem['children'])
                if elem['type'] == 'S':
                    src.extend(src_sub)
                else:
                    src.extend(tgt_sub)
                tgt.extend(tgt_sub)

    if incorrect is not None or correct is not None:
        if isinstance(incorrect, tuple):
            src.extend(incorrect[0])
        else:
            src.append(incorrect)

        if isinstance(correct, tuple):
            tgt.extend(correct[1])
        else:
            tgt.append(correct)

    return src, tgt


def main():
    for line in sys.stdin:
        line = line.strip()
        match = re.match('<p>(.*)</p>', line)
        if not match:
            continue
        text = match.group(1)
        tokens = tokenize(text)
        tree = parse(tokens)
        src, tgt = generate_typo_pair(tree)
        i = ''.join(token for token in src if token is not None)
        c = ''.join(token for token in tgt if token is not None)
        if i != c:
            print(f'{i}\t{c}')


if __name__ == '__main__':
    main()
