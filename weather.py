#!/usr/bin/python

import re
import urllib
import json,requests
import argparse
import sys

ARG_LOCATION=''
ARG_UNIT=1 #use 1 for F 0 for C
ARG_ALL=1
ARG_CURRENT=1
ARG_FORECAST=0
ARG_SUN=1
ARG_DEFAULT_ALL=1
 echo "Usage: [-h] [-l locations] [-u unit] [-a|-c|-d days|-s]"
    echo "-h Print this page"
    echo "-l Set locations"
    echo "-u Set unit c or C or f or F"
    echo "-a Equal to -c -d5 -s"
    echo "-c Current Condition"
    echo "-d Set forecast days"
    echo "-s Print Sunrise/Sunset times"

def main(argv):
    parser = argparse.ArgumentParser(
        description="Examples of argparse usage",
        epilog="With a message at the end" )

if __name__ == "__main__":
    main(sys.argv[1:])
