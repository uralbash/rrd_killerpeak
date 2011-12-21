#import easy to use xml parser called minidom:
import os
import sys
import shutil
from time import time
from xml.dom import minidom

def cutPeak(xml, *args):

    doc = minidom.parse(xml)
    database = doc.getElementsByTagName("row")
    ds = doc.getElementsByTagName("ds")

    dsnamed = []
    for data in ds:
        if data.parentNode.nodeName == 'rrd':
            dsnamed.append(data.getElementsByTagName("name")[0].firstChild.data)

    nodelen = len(database[0].getElementsByTagName('v'))
    if nodelen != len(args):
        print "You must have %d argument values." % nodelen
        print "example: python killerpeak.py <rrd file> arg1 arg2 ..."
        sys.exit(0)

    for i, arg in enumerate(args):
        if int(arg):
            for row in database:
                value = row.getElementsByTagName('v')
                data = float(value[i].firstChild.data)

                if data >= float(arg):
                    print "ds: %s | detect peak: %s"\
                            % (dsnamed[i], data)
                    value[i].firstChild.nodeValue = 'NaN'

    return doc

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        print "PLease run command like:"
        print "python killerpeak.py <rrd file> arg1 arg2 ..."
        sys.exit(0)

    # create rrd dump
    olddoc = "old.xml"
    rrd_dump = os.system("rrdtool dump '%s' > '%s'" % (filename, olddoc))

    # cut peak
    newdoc = cutPeak(olddoc, *sys.argv[2:])
    f = open('new.xml', 'w')
    newdoc.writexml(f)
    f.close()

    # backup rrd
    bakdir = 'rrd_bak'
    if not os.path.exists(bakdir):
        os.makedirs(bakdir)
    dir = os.path.join(bakdir, str(int(time())))
    os.makedirs(dir)
    shutil.copy2(filename, dir)

    # restore rrd
    os.unlink(filename)
    os.system("rrdtool restore 'new.xml' '%s'" % filename)
    os.unlink('new.xml')
    os.unlink('old.xml')

