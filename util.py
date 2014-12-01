#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import pprint
import logging
import inspect

_logger = None

def log(obj):
    _func = "[%s():%s] " % (inspect.stack()[1][3], inspect.stack()[1][2])
    global _logger
    if not _logger:
        _logger = logging.getLogger()
        s = logging.StreamHandler( sys.stderr )
        _logger.addHandler(s)
        _logger.setLevel(logging.DEBUG)
        s.setFormatter(logging.Formatter( '%(asctime)s %(levelname)s %(message)s' ) )

    _logger.debug(_func + (obj if type(obj) == str or type(obj) == unicode else str(obj)))

def set_utf8_to_stdio():
    import codecs
    sys.stdin = codecs.getreader('utf_8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

def set_utf8_to_stderr():
    import codecs
    sys.stderr = codecs.getwriter('utf_8')(sys.stderr)
    
def pp(obj):
    import re
    pp = pprint.PrettyPrinter(indent=4, width=200)
    str = pp.pformat(obj)
    return re.sub(
        r"\\x([0-9a-f]{2})", lambda x: unichr(int("0x"+x.group(1), 16)), 
        re.sub(r"\\u([0-9a-f]{4})", lambda x: unichr(int("0x"+x.group(1), 16)), str)
        )

    # return eval("u''' %s '''" % str).strip()

def ppp(*objs):
    for obj in objs:
        print pp(obj)

def optparse(args):
    dict = {}
    prev = None
    for arg in args[1:]:
        if arg[0:1] == "-":
            if prev:
                dict[prev] = True
            prev = arg
        else:
            if prev:
                dict[prev] = arg
                prev = None
            else:
                # error
                pass
    if prev:
        dict[prev] = True

    return dict

def zshrun(cmd):
    import subprocess
    
    stdio = subprocess.Popen(['/usr/bin/zsh'],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             close_fds=True).communicate(cmd)
    # log(stdio[1])
    return stdio

def jaccard_s(x, y):
    if len(x) == 0 or len(y) == 0:
        return 0.0

    numerator = 0.0
    if len(x) > len(y):
        vs = y; vl = x
    else:
        vs = x; vl = y

    for key in vs:
        if key in vl:
            numerator += vs[key] if vs[key] < vl[key] else vl[key]

    vs_sum = reduce(lambda x, y: x+y, vs.values())
    vl_sum = reduce(lambda x, y: x+y, vl.values())

    return 1.0*numerator / (vs_sum + vl_sum - numerator)

def _test_jaccard_s():
    vec1 = {u"a": 1.0, u"b": 2.0, u"c": 1.0}
    vec2 = {           u"b": 1.0,           u"d": 1.0}
    vec3 = {u"a": 1.0,            u"c": 2.0,u"d": 2.0}

    print jaccard_s(vec1, vec2)
    print jaccard_s(vec1, vec3)
    print jaccard_s(vec2, vec3)
