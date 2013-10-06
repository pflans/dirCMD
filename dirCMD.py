import os
import sys
import json
import argparse
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
from pprint import pprint

def nodot(item): return item[0] != '.'

def walker(tree, branches, node):
    if len(branches) == 1:
        tree[branches[0]] = node
        return
    if not branches[0] in tree:
        tree[branches[0]] = {}
    walker(tree[branches[0]], branches[1:], node)
    
    
def buildTree(tree, startpath):
    startdir = startpath.split('/')[-1]
    for root, dirs, files in os.walk(startpath):
        if verbose:
            path = root.split('/')
            print root       
            for file in files:
                print str(root) + str(file)
        branches = [startdir]
        if root != startpath:
            branches.extend(os.path.relpath(root, startpath).split('/'))
        walker(tree, branches, dict([(d,{}) for d in dirs]+ \
                                      [(f,os.path.splitext(f)[1]) for f in filter(nodot, files)]))
def xmlBuilder(tree):
    for key, value in tree.iteritems():
        if isinstance(value, dict):
            print '<directory name="%(name)s">' %{"name": key}
            xmlBuilder(value)
            print '</directory>'
        else:
            print '<file name="%(name)s">' %{"name": key}
            print '<attribute extension="%(ext)s">' %{"ext": value}
            print '</file>'
            
def main(argv):   
    global verbose
    parser = argparse.ArgumentParser(description='Print a directory tree.')
    parser.add_argument('path', metavar='P',
                       help='starting path for the tree traversal')
    parser.add_argument('-v', '--verbose', help='print directory traversal', action="store_true")

    args = parser.parse_args()
    verbose = args.verbose
    path = args.path 
    
    tree = {}
    buildTree(tree, path)

    xmlBuilder(tree)
    #json.dumps(tree)
        
if __name__ == '__main__':
    
    main(sys.argv[1:])