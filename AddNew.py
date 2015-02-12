# -*- coding: utf-8 -*-
#!/usr/bin/env python2.7

import dataconnection
import sys

db = dataconnection.DataConnection()

def recipeFromFile(file):
    with open(file, 'r') as fin:
        mode = 0
        name = ''
        ingr = ''
        rcpe = ''
        tags = []
        
        for line in fin:
            if line == '\n':
                mode += 1
            elif mode == 0:
                name = line
            elif mode == 1:
                ingr += line
            elif mode == 2:
                rcpe += line
            elif mode == 3:
                tags.append(line)

    name = name[:-1]
    print '+', name,
    try:
        result = db.addRecipe(name, ingr, rcpe, (','.join(tags)).replace('\n', ''))
        print ' ok'
        return result
    except dataconnection.ExistsAlready:
        print ' skipped'
        return 'ERROR'

if __name__ == '__main__':
    if not len(sys.argv) > 1:
        print('%s <Datei>')
        sys.exit(1)

    fileNames = sys.argv[1:]
    for file in fileNames:
        recipeFromFile(file)
