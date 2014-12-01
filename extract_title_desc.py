import sys
import util

util.set_utf8_to_stdio()

pageinfo = None
in_text = False

def clean_text(text):
    new_text = None
    inside_infobox = False
    for line in text:
        if line[0:2] == "{{" and line[-2:] == "}}":
            continue
        if line[0:2] == "[[" and line[-2:] == "]]":
            continue
        if line == u'':
            continue
        if line[0:7] == u'&lt;!--':
            continue
        if line[0:2] == "{{":
            inside_infobox = True
            continue
        if line[-2:] == "}}" and "{{" not in line:
            inside_infobox = False
            continue
                
        if not inside_infobox:
            new_text = line
            break
    if new_text == None:
        new_text = "" 
    return new_text.replace(u'\t', '  ')


for line in sys.stdin:
    line = line.strip()
    if line == "<page>":
        pageinfo = {}
        in_text = False
    elif line[0:7] == "<title>":
        pageinfo['title'] = line[7:-8]
    elif line[0:4] == "<ns>":
        pageinfo['ns'] = line[4:-5]
    elif line[0:4] == "<id>":
        if 'id' not in pageinfo:
            pageinfo['id'] = line[4:-5]
    elif line[0:6] == "<text ":
        pageinfo['buf'] = [line[27:]]
        in_text = True
    elif line == "</page>":
        if pageinfo['ns'] == u'0':
            pageinfo['text'] = clean_text( pageinfo['buf'] )
            del pageinfo['buf']
            print "\t".join( [pageinfo['id'], pageinfo['title'], pageinfo['text']] )
            # print util.pp( pageinfo )
    else:
        if in_text:
            pageinfo['buf'].append( line )
            
        
