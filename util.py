# /usr/bin/env python
# -*- coding: UTF-8 -*-
# ylin 2018.6.26

import json, os, sys
reload(sys)
sys.setdefaultencoding('utf-8')

def readJsonFile(file):
    if False == os.path.exists(file):
        return {}
    f = open(file, 'r')
    contents = f.read()
    jsonObj = json.loads(contents)
    f.close()
    return jsonObj


def writeLinesFile(lines, file):

    dir = os.path.dirname(file)
    if False == os.path.exists(dir):
        os.makedirs(dir)

    fp = open(file, 'w')
    for i in range(len(lines)):
        fp.write(lines[i] + '\n')
    fp.flush()
    fp.close()

def space(lel, type='tab'):
    speed = '    '
    ret = ''
    for l in range(0, lel):
        ret += speed

    return ret