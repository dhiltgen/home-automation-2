#!/usr/bin/python

import argparse
import glob
import json
import logging
import os
import subprocess
import sys
import time

log = logging.getLogger(__name__)


def main():
    """
    Read one or more sensors, and queue for servers to later upload
    """
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('--conf', default="/etc/sensors.json",
                        help="The local json config file for this system")
    parser.add_argument('--verbose', action="store_true",
                        help="Turn on verbose output")
    parser.add_argument('--interval', default=120,
                        help="How many seconds to sleep between gathering data")
    args = parser.parse_args()

    # Make sure the file exists, or create an example and exit
    if not os.path.exists(args.conf):
        print 'ERROR: No configuration exists\n'
        sys.exit(1)

    while True:
        # Get UTC epoch time
        now = time.mktime(time.gmtime(time.time()))
        if args.verbose:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)


        with open(args.conf, "r") as fd:
            conf = json.loads(fd.read())

        # Gather the readings...
        for sensor in conf['sensors']:
            sensor['val'] = str(subprocess.check_output([
                'owread', '-F', '-s', sensor['server'], sensor['path']])).strip()
            log.debug("Sensor %r current reading %r", sensor['type'],
                    sensor['val'])

        # Now update each servers queues
        for server in conf['servers']:
            with open(server['local_queue'], "a") as readings:
                for sensor in conf['sensors']:
                    readings.write("%s,location=%s value=%f %ld\n" % (
                        sensor['type'], sensor['location'],
                        float(sensor['val']), int(now)))
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
