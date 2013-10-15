import os
from lxml import etree
import sys
import json
import argparse
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
from pprint import pprint

def nodot(item): return item[0] != '.'

def buildTree(path):
    basename = os.path.basename(path)
    node = etree.Element("node")
    node.attrib['name'] = basename.decode('utf-8')
    if os.path.isdir(path):
        # Recurse
        node.tag = 'dir'
        for item in sorted(os.listdir(path)):
            item_path = os.path.join(path, item)
            child_node = buildTree(item_path)
            node.append(child_node)
        return node
    else:
        node.tag = 'file'
        return node    

            
def main(argv):   
    global verbose
    parser = argparse.ArgumentParser(description='Print a directory tree.')
    parser.add_argument('path', metavar='P',
                       help='starting path for the tree traversal')
    parser.add_argument('-v', '--verbose', help='print directory traversal', action="store_true")

    args = parser.parse_args()
    verbose = args.verbose
    path = args.path 


    root = buildTree(path)
    
    # Create an element tree from the root node
    # (in order to serialize it to a complete XML document)
    tree = etree.ElementTree(root)
    
    xml_document = etree.tostring(tree,
                                  pretty_print=True,
                                  xml_declaration=True,
                                  encoding='utf-8')
    print xml_document
   
    #json.dumps(tree)
        
if __name__ == '__main__':
    
    main(sys.argv[1:])