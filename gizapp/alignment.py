"""
Data access methods for reading GIZA++ result files.
"""
import re

def read_alignment_file(io):
    """Read GIZA++'s *.A.final (Viterbi alignment) file and returns the alignment object per each
    sentence pair.'

    Parameters:
        io (file): the file object (or sys.stdin) from which to read *.A.* file.

    Returns:
        list of dict which has the following keys:

    """
    num_sent = 0
    spairs = []
    for line in io:
        m = re.match(r'# Sentence pair \((\d+)\) source length (\d+) target length (\d+) '
                     r'alignment score : ([\.\de\-]+)', line)
        assert m, 'Malformed header line: %s' % line

        sent_id = int(m.group(1))
        assert sent_id == num_sent + 1, 'Sentence pair number does not match: %s' % line

        source_length = int(m.group(2))
        target_length = int(m.group(3))
        alignment_score = float(m.group(4))
        line = next(io)
        target_sent = line.rstrip()
        line = next(io)
        source_sent = line.rstrip()
        source_tokens = []
        for m in re.finditer(r'([^ ]+) \(\{(.*?)\}\) ', source_sent):
            token = m.group(1)
            pos_list = [int(s) for s in m.group(2).strip().split(' ') if s != '']
            source_tokens.append((token, pos_list))
        spairs.append({'sent_id': sent_id,
                       'source_length': source_length, 'target_length': target_length,
                       'alignment_score': alignment_score,
                       'target_sent': target_sent, 'source_sent': source_sent,
                       'source_tokens': source_tokens})
        num_sent += 1
    return spairs


if __name__ == '__main__':
    import sys
    fields = ['sent_id', 'source_length', 'target_length', 'alignment_score',
              'target_sent', 'source_sent', 'source_tokens']
    for spair in read_alignment_file(sys.stdin):
        print '\t'.join([str(spair[field]) for field in fields])
