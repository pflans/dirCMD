import os
import sys
import json
import argparse
from xml.sax.saxutils import quoteattr as xml_quoteattr
from collections import defaultdict
from pprint import pprint

def set_leaf(root, dirs, item):

    if len(dirs) == 1:
        root[dirs[0]] = item
        return
    if not root.has_key(dirs[0]):
        root[dirs[0]] = {}
    set_leaf(root[dirs[0]], dirs[1:], item)

def main(argv):                         
    parser = argparse.ArgumentParser(description='Print a directory root.')
    parser.add_argument('path', metavar='P',
                       help='starting path for the root traversal')
    parser.add_argument('-v', '--verbose', help='print directory traversal process (increases running time)', action="store_true")

    args = parser.parse_args()
    verbose = args.verbose
    path = args.path 
  
    startpath = path
    root = {}
    for root, dirs, files in os.walk(startpath):
        dirs = [startpath]
        if root != startpath:
            dirs.extend(os.path.relpath(root, startpath).split('/'))
    
        set_leaf(root, dirs, dict([(d,{}) for d in dirs]+ \
                                      [(f,None) for f in files]))
        
    pprint(root)
    

        
if __name__ == '__main__':
    
    main(sys.argv[1:])