"""
Given a plan text file (output of xml2text.py and clean_text.py), regard two consecutive lines
as a question and an answer, and turn them into a bitext. For example, this will turn:
    sent1
    sent2
    sent3
    sent4
into
    sent1   sent2
    sent2   sent3
    sent3   sent4

Empty lines are considered as separators. For example,
    sent1
    sent2
    [empty line]
    sent3
    sent4
will be:
    sent1   sent2
    sent3   sent4
and (sent2, sent3) won't be created.
"""

def main(io):
    prev_line = None
    for line in io:
        line = line.strip()
        if line:
            if prev_line:
                print '%s\t%s' % (prev_line, line)
            prev_line = line
        else:
            prev_line = None

if __name__ == '__main__':
    import sys
    import codecs
    sys.stdin = codecs.getreader('utf_8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
    main(sys.stdin)
