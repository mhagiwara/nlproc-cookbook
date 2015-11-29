"""
Data access methods for reading GIZA++ result files.
"""
from collections import defaultdict


def read_ttable_file(io):
    """Read GIZA++'s *.ti.final (final inverse T-table) file and returns the T-table object with
    lexical translation probabilities.

    Parameters:
        io (file): the file object (or sys.stdin) from which to read *.ti.final file.

    Returns:
        dict from target word to a dict from source word to a probability

    """
    ttable = defaultdict(dict)
    for line in io:
        tword, sword, prob_str = line.rstrip().split(' ')
        ttable[tword][sword] = float(prob_str)
    return ttable


if __name__ == '__main__':
    import sys
    ttable = read_ttable_file(sys.stdin)
    for tword, sworddict in ttable.iteritems():
        for sword, prob in sworddict.iteritems():
            if prob > 0.8:
                print '%s\t%s\t%s' % (tword, sword, prob)
