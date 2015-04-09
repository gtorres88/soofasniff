import getopt
import logging
import sys
import datetime
from kisconnect import *

logger = logging.getLogger()
logging.basicConfig(
    filename=None,
    format='%(asctime)s |%(levelname)7s |%(name)20s | %(message)s')

logger.setLevel(logging.DEBUG)

from kisresponse import *


argList = ['help', 'output=', 'server=', 'port=']

def usage():
    print "Usage: python csvscript -o outputfile [OPTIONS]"
    print "-h, help\n\tDisplays this menu"
    print "-o, --output\n\tSpecifies output file"
    print "-s, --server\n\tSpecifies kismet server, localhost is default"
    print "-p, --port \n\tSpecifies port, 2501 is default"


def main(argv):


    outputFile = None
    server = 'localhost'
    port = 2501

    try:
        opts, args = getopt.getopt(argv, "ho:s:p:", argList)
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif opt in ("-o", "--output"):
            outputFile = arg
        elif opt in ("-s", "--server"):
            server = arg
        elif opt in ("-p", "--port"):
            port = int(arg)

    if outputFile is None:
        print "Please provide output file"
        usage()
        sys.exit(2)

    csv = open(outputFile, "w")

    K = KismetConnect()
    K.open()

    #Stop automatic time messages
    K.send_cmd("REMOVE TIME")
    #Start subscribe to client detection messages
    K.send_cmd("ENABLE CLIENT mac,lasttime")
    
    try:
        while(1):
            r = K.process_incoming()

            if (isinstance(r, ClientResponse)):
                mac = r.params[0]
                time = datetime.datetime.fromtimestamp(int(r.params[1]))
                towrite = "%s, %s\n" % (r.params[0],str(time))
                logger.debug("Writing to CSV: %s" % towrite)
                csv.write(towrite)
    except KeyboardInterrupt:
        csv.close()
        logger.info("Crtl-C caught. Exiting")


if __name__ == '__main__':
    if (len(sys.argv) < 2):
        usage()
        sys.exit(2)
    main(sys.argv[1:])
