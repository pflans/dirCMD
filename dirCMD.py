import os
import sys
import argparse
from xml.sax.saxutils import quoteattr as xml_quoteattr

# Settings


# Does not return items that have a period as the first character (used to ignore OS X hidden files)
def nodot(item): return item[0] != '.'



def xmlCrawler(path):
    result = ''
    for item in filter(nodot, os.listdir(path)):
        itempath = os.path.join(path, item)
        # If the program comes across another subdirectory it restarts the script and continues down the tree
        if os.path.isdir(itempath):
            result += '<dir name="'+xmlCrawler(itempath)+'">'
        # If the program comes across a file it uses the file's path to pull out the file name and give it a "file" classification
        elif os.path.isfile(itempath):
            result += '<file name="'+item+'">'
    
    #Adds closing markup after the loop
    output = result
    return output


def main(argv):                         
    parser = argparse.ArgumentParser(description='Print a directory tree.')
    parser.add_argument('path', metavar='P',
                       help='starting path for the tree traversal')
    parser.add_argument('-v', '--verbose', help='print directory traversal process (increases running time)', action="store_true")

    args = parser.parse_args()
    verbose = args.verbose
    path = args.path 
  

    #try:                                
    #    opts, args = getopt.getopt(argv, "hp:v", ["help", "path="]) 
    #except getopt.GetoptError:           
    #    usage()                          
    #    sys.exit(2)   

    print path  
    print xmlCrawler(path)
    
    # Flags: output file location and name, path, verbose, help, json/xml/other?
        
        
if __name__ == '__main__':
    
    main(sys.argv[1:])
    
    
    
    
