# coding=utf-8
import sys
import codecs
import re
import unicodedata
from itertools import izip


def is_katakana(ch):
    """Return True if and only if ch is a Katakana letter."""
    assert len(ch) == 1
    return unicodedata.name(ch).startswith('KATAKANA LETTER')


def is_katakana_title(title):
    """Return True if and only if title is all Katakana letters."""
    return all(is_katakana(ch) or ch in [' ', u'・', u'ー'] for ch in title)


def clean_title(title):
    """Clean the title by stripping out brackets and lowercasing."""
    title = re.sub(r' \(.*\)', '', title)
    return title.lower()


def align_titles(en_title, ja_title):
    """Align English and Japanese titles, then yield over pairs of chunks.
    For example, if titles are ('XX YY', 'ZZ WW'), then this iterates over ('XX', 'ZZ'), and
    ('YY', 'ZZ'). Returns immediately if the numbers of chunks are different between the two."""
    en_title_chunks = en_title.split(' ')
    ja_title_chunks = ja_title.split(u'・')
    if len(en_title_chunks) != len(ja_title_chunks):
        return iter(())

    return izip(en_title_chunks, ja_title_chunks)


def main():
    """Main entrypoint of this script."""
    for line in sys.stdin:
        fields = line.strip().split('\t')

        # Skip invalid row (with a different number of fields)
        if len(fields) != 4:
            continue

        _, en_title, ja_title, _ = fields

        # Strip the first 'en:'
        if en_title.startswith('en:'):
            en_title = en_title[3:]

        # Skip if either English or Japanese field is empty.
        if not en_title or not ja_title:
            continue

        en_title, ja_title = clean_title(en_title), clean_title(ja_title)

        # Skip non-Katakana titles.
        if not is_katakana_title(ja_title):
            continue

        if '#' in en_title:
            continue

        for en_chunk, ja_chunk in align_titles(en_title, ja_title):
            print '%s\t%s' % (' '.join(en_chunk), ' '.join(ja_chunk))


if __name__ == '__main__':
    sys.stdin = codecs.getreader('utf_8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
    main()
