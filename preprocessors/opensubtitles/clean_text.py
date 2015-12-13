"""
Given a plan text file (output of xml2text.py), clean sentences. Specifically,
    - remove preceding '-'
    - remove entire lines in brackets [ ] or ()
    - remove entire lines if starts with 'Subtitle by'
    - remove entire lines if contains '<i>' (monologues)
    - untokenize sentence
"""


def detokenize(tokens):
    """Given a list of tokens, returns text that is untokenized."""
    if not tokens:
        return ''

    tokens = list(tokens) + ['']    # add sentinel
    merged_tokens = []
    i = 0
    token = tokens[0]
    while i < len(tokens) - 1:
        merge = False
        next_token = tokens[i+1]

        if next_token in [',', '.', '?', '!', '!!', ':']:
            merge = True
        if token[-1] == "'" and next_token in ['s', 're', 'm', 't', 've', 'd']:
            merge = True
        if token[-1] == "'" and next_token in ['il']:   # OCR error?
            next_token = 'll'
            merge = True
        if token[-1] == '-':
            merge = True

        if merge:
            token += next_token
            i += 1
        else:
            merged_tokens.append(token)
            i += 1
            token = tokens[i]

    return merged_tokens


def clean_line(line):
    if not line:
        return ''

    if line.startswith('- '):
        line = line[2:]

    if line[0] == '[' or line[-1] == ']':
        return ''

    if line[0] == '(' or line[-1] == ')':
        return ''

    if '<i>' in line or '</ i>' in line:
        return ''

    if line.startswith('Subtitle by'):
        return ''

    # detokenize
    if line:
        line = ' '.join(detokenize(line.split(' ')))

    return line


def main(io):
    for line in io:
        print clean_line(line.rstrip())

if __name__ == '__main__':
    import sys
    import codecs
    sys.stdin = codecs.getreader('utf_8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
    main(sys.stdin)
