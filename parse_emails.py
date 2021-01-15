import os
import re
import argparse
import logging
import ipaddress
from email.parser import FeedParser
from email.feedparser import BytesFeedParser

parser = argparse.ArgumentParser(description="""
Email parser. 
This script helps you to parse emails.
""")


group = parser.add_mutually_exclusive_group()
group.add_argument('--header-pattern',
                   help='parse the headers', dest='pattern')
group.add_argument('--header-string',
                   help="parse the string", dest='string')
parser.add_argument('-e', help='path to file', dest='path')
group.add_argument('-ip', help='parse to find ip',
                   action='store_true', dest='ip')
parser.add_argument('-l', help='logging', dest='log', default='WARNING',
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])

args = parser.parse_args()

logging.basicConfig(filename='parser.log', level=getattr(logging, args.log.upper()),
                    format='%(asctime)s -  %(levelname)s - %(message)s')

pattern = args.pattern
filename = args.path

if args.pattern:
    logging.info(args.pattern)
    logging.debug('pattern there')
    logging.warning(args.path)
    logging.warning(header_info)
    with open(filename, 'r') as file:
        raw_lines = file.readlines()
    for line in raw_lines:
        if re.search(pattern, line):
            print(line)

elif args.string:
    logging.info(args.string)
    logging.debug('string there')
    logging.warning(args.path)

if args.log:
    logging.critical(args.log)
    logging.debug('log there')

if args.ip:
    logging.debug('ip there')
    with open(filename, 'r') as file:
        raw_lines = file.readlines()
    for line in raw_lines:
        addresses = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", line)
        # domain = re.findall("@[\w.]+", line)
        # print(domain)
        # logging.warning(domain)
        for address in addresses:
            if ipaddress.ip_address(address):
                print(address)
                logging.warning(address)
