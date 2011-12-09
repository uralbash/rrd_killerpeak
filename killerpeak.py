#!/usr/bin/env python
import os
import shutil
from xml.etree import ElementTree as ET
from optparse import OptionParser

__version__ = '0.1'

def get_configuration():
    parser = OptionParser(version="%prog v" + __version__,
                          usage="%prog <filename>")
    parser.add_option("-v", "--verbose", action="count", default=0,
                      help="produce more output")
    parser.add_option('-b', '--border', action ='store', default=10**10,
                 help='Min value of peak. Default 100000')
    options, args = parser.parse_args()

    if not os.path.isfile(args[0]):
        parser.error("Not found file")

    return [ options ] + args

def main():
    options, filename = get_configuration()
    try:
        rrd_dump = os.system("rrdtool dump '%s' > 'old.xml'" % (filename))
    except:
        print "Error RRD file type"
        raise

    if not os.path.exists('rrd_bak'):
        os.makedirs('rrd_bak')
    shutil.copy2(filename, 'rrd_bak')

    tree = ET.parse('old.xml')

    def iterparent(tree):
        for parent in tree.getiterator():
            for child in parent:
                yield parent, child

    for parent, child in iterparent(tree):
        if child.tag == 'v':
            if float(child.text) > options.border:
                print 'peak detect in %s' % filename
                child.text = 'NaN'

    tree.write('new.xml')
    os.unlink(filename)
    os.system("rrdtool restore 'new.xml' '%s'" % filename)
    os.unlink('new.xml')
    os.unlink('old.xml')

if __name__ == '__main__':
    import sys
    sys.exit(main())
