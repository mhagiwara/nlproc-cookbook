import sys

import editdistance
from collections import namedtuple

Edit = namedtuple('Cell', ['type', 'dist', 'total', 'src', 'tgt', 'prev'])


def align_tokens(source, target):

    len1, len2 = len(source), len(target)
    cells = [[None for _ in range(len2+1)] for _ in range(len1+1)]
    cells[0][0] = Edit(type=None, dist=0, total=0, src=None, tgt=None, prev=None)

    total_dist = 0
    for i in range(len1):
        cells[i+1][0] = Edit(type='delete', dist=len(source[i]), total=total_dist,
                             src=source[i], tgt=None, prev=(i, 0))
        total_dist += len(source[i])

    total_dist = 0
    for j in range(len2):
        cells[0][j+1] = Edit(type='insert', dist=len(target[j]), total=total_dist,
                             src=None, tgt=target[j], prev=(0, j))
        total_dist += len(target[j])

    for i in range(len1):
        for j in range(len2):

            # edit_dist = editdistance.eval(source[i], target[j])
            edit_dist = 1 if source[i] != target[j] else 0

            mis_cell = cells[i][j+1]
            xtr_cell = cells[i+1][j]
            wrg_cell = cells[i][j]

            cells[i+1][j+1] = min(
                Edit(type='delete', dist=len(source[i]), total=mis_cell.total+len(source[i]),
                     src=source[i], tgt=None, prev=(i, j+1)),
                Edit(type='insert', dist=len(target[j]), total=xtr_cell.total+len(target[j]),
                     src=None, tgt=target[j], prev=(i+1, j)),
                Edit(type=('match' if edit_dist==0 else 'subst'), dist=edit_dist,
                     total=wrg_cell.total+edit_dist, src=source[i], tgt=target[j], prev=(i, j)),
                key=lambda cell: cell.total)

    path = []
    curr_cell = cells[len1][len2]
    while curr_cell.prev != None:
        path.insert(0, curr_cell)
        curr_cell = cells[curr_cell.prev[0]][curr_cell.prev[1]]

    return path

TYPE2SIGN = {
    'match': '=',
    'subst': '*',
    'delete': '-',
    'insert': '+'
}


def main():
    for line in sys.stdin:
        fields = line.strip().split('\t')
        if len(fields) != 3:
            continue
        code, incorrect, correct = fields

        incorrect_tokens = list(incorrect.lower().replace(' ', '_'))
        correct_tokens = list(correct.lower().replace(' ', '_'))
        edits = align_tokens(incorrect_tokens, correct_tokens)

        non_match_edits = [i for i, edit in enumerate(edits) if edit.type != 'match']
        if not non_match_edits:
            continue
        lower = min(non_match_edits)
        upper = max(non_match_edits)
        lower = max(0, lower-30)
        upper = min(len(edits)-1, upper+30)

        diffs = []
        src = []
        tgt = []
        for edit in edits[lower:upper+1]:
            diffs.append('{}/{}/{}'.format((edit.src or ''),
                                           (edit.tgt or ''),
                                           TYPE2SIGN[edit.type]))
            src.append(edit.src or '')
            tgt.append(edit.tgt or '')

        print('{}\t{}\t{}\t{}'.format(code, ''.join(src), ''.join(tgt), ' '.join(diffs)))

if __name__ == '__main__':
    main()
