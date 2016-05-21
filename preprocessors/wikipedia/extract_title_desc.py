"""
Script to clean up Wikipedia dump file *-pages-meta-current.xml and returns a TSV of
ID, title, and the first paragraph. This takes the uncompressed XML file from STDIN and
outputs the cleaned-up TSV to STDOUT.
"""
import sys
import codecs


def clean_text(lines):
    """Given a list of lines, clean it and returns a cleaned string."""
    new_text = None
    inside_infobox = False
    for line in lines:
        if line.startswith('{{') and line.endswith('}}'):
            continue
        if line.startswith('[[') and line.endswith(']]'):
            continue
        if not line:
            continue
        if line.startswith('&lt;!--'):
            continue
        if line.startswith('{{'):
            inside_infobox = True
            continue
        if line.endswith('}}') and '{{' not in line:
            inside_infobox = False
            continue

        if not inside_infobox:
            new_text = line
            break
    if new_text is None:
        new_text = ''
    return new_text.replace(u'\t', '  ')


def main():
    """Main entrypoint of this script."""
    pageinfo = None
    in_text = False

    for line in sys.stdin:
        line = line.strip()
        if line == '<page>':
            pageinfo = {}
            in_text = False
        elif line.startswith('<title>'):
            pageinfo['title'] = line[7:-8]
        elif line.startswith('<ns>'):
            pageinfo['ns'] = line[4:-5]
        elif line.startswith('<id>'):
            if 'id' not in pageinfo:
                pageinfo['id'] = line[4:-5]
        elif line.startswith('<text '):
            pageinfo['buf'] = [line[27:]]
            in_text = True
        elif line == '</page>':
            if pageinfo['ns'] == '0':
                pageinfo['text'] = clean_text(pageinfo['buf'])
                del pageinfo['buf']
                print "\t".join([pageinfo['id'], pageinfo['title'], pageinfo['text']])
        else:
            if in_text:
                pageinfo['buf'].append(line)

if __name__ == '__main__':
    sys.stdin = codecs.getreader('utf_8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
    main()
