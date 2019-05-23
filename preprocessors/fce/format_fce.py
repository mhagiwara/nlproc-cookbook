import sys
import re

def tokenize(xmltext):
    tokens = []
    for match in re.finditer(r'</?[^>]*>|[^/<>]*', xmltext):
        if match.group(0):
            tokens.append(match.group(0))

    return tokens


def parse(tokens):
    stack = [{'children': []}]
    for token in tokens:
        if token.startswith('<') and not token.startswith('</'):
            if token[1:3] == 'NS':
                type = token.split('"')[1]
                elem = {'tag': 'NS', 'type': type, 'children': []}
            else:
                elem = {'tag': token[1:2], 'children': []}
            stack.append(elem)
        elif token.startswith('</'):
            tag = token[2:-1]
            if stack[-1]['tag'] == tag:
                elem = stack.pop()
                stack[-1]['children'].append(elem)
        else:
            stack[-1]['children'].append(token)
    return stack[-1]['children']


def generate_pairs(tree):
    pairs = [(None, [], [])]
    correct = None
    incorrect = None
    for elem in tree:
        if isinstance(elem, str):
            new_pairs = []
            for t, i, c in pairs:
                new_pairs.append((t, i + [elem], c + [elem]))
            pairs = new_pairs
        if isinstance(elem, dict):
            if elem['tag'] == 'i':
                if len(elem['children']) == 1 and isinstance(elem['children'][0], str):
                    incorrect = elem['children'][0]
                else:
                    incorrect = generate_pairs(elem['children'])
            elif elem['tag'] == 'c':
                correct = elem['children'][0]
            elif elem['tag'] == 'NS':
                sub_pairs = generate_pairs(elem['children'])
                new_pairs = []
                for t1, i1, c1 in pairs:
                    for t2, i2, c2 in sub_pairs:
                        if t1:
                            new_pairs.append((t1, i1 + c2, c1 + c2))
                        else:
                            new_pairs.append((t2 or elem['type'], i1 + i2, c1 + c2))
                            new_pairs.append((t1, i1 + c2, c1 + c2))
                pairs = new_pairs

    if incorrect != None or correct != None:
        pairs = []
        if isinstance(incorrect, list):
            pairs.extend(incorrect)
            sub_corrects = set(tuple(c) for _, _, c in incorrect)
            for sub_correct in sub_corrects:
                pairs.append(([], list(sub_correct), [correct]))
        else:
            pairs = [(None, [incorrect], [correct])]

    return [(t, i, c) for (t, i, c) in pairs if i != c]


def main():
    for line in sys.stdin:
        line = line.strip()
        match = re.match('<p>(.*)</p>', line)
        if not match:
            continue
        text = match.group(1)
        tokens = tokenize(text)
        tree = parse(tokens)
        pairs = generate_pairs(tree)
        for t, i, c in pairs:
            if any(isinstance(token, dict) for token in i + c):
                continue
            i = ''.join(token for token in i if token is not None)
            c = ''.join(token for token in c if token is not None)
            print('{}\t{}\t{}'.format(t, i, c))


if __name__ == '__main__':
    main()
