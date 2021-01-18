import re
import email
import argparse
import logging
from collections import Counter


parser = argparse.ArgumentParser(description="""
Email parser. 
This script helps you to parse emails.
""")


group = parser.add_mutually_exclusive_group()
group.add_argument('--header-pattern',
                   help='parse the headers', dest='pattern')
group.add_argument('--header-string',
                   help="parse the string", dest='string')
group.add_argument('-ip', help='parse to find ip',
                   action='store_true', dest='ip')
parser.add_argument('-e', help='path to file', dest='path')
parser.add_argument('-l', help='logging', dest='log', default='WARNING',
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])

args = parser.parse_args()

logging.basicConfig(filename='parser.log', level=getattr(logging, args.log.upper()),
                    format='%(asctime)s -  %(levelname)s - %(message)s')


def get_header(fname):
    """
    opens file with mail content inside
    returns email in a string representation
    """
    with open(fname, 'r') as file_mail:
        email_message = email.message_from_file(file_mail)
    email_parser = email.parser.HeaderParser()
    return email_parser.parsestr(email_message.as_string())


if args.pattern:
    print(args.pattern)
    logging.info(args.pattern)
    logging.debug('pattern there')
    logging.warning(args.path)
    headers = get_header(args.path)
    header_string = headers.as_string()
    print(re.findall(args.pattern + '.*\n', header_string))


elif args.string:
    logging.info(args.string)
    logging.debug('string there')
    logging.warning(args.path)
    headers = get_header(args.path)
    print(headers.get(args.string))

elif args.ip:
    logging.debug('ip there')
    headers = get_header(args.path)
    header_string = headers.as_string()
    domains = re.findall(r'@[\w.]+', header_string)
    domains = [domain.replace('@', '') for domain in domains]
    count_dom = Counter(domains)
    addresses = re.findall(
        r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", header_string)
    count_addr = Counter(addresses)
    print('\nDomain\t\tCount')
    for k, v in count_dom.items():
        print('%-9s \t %-9s' % (k, v))
    print('\nIP\t\tCount')
    for k, v in count_addr.items():
        print('%-9s \t %-9s' % (k, v))

if args.log:
    logging.critical(args.log)
    logging.debug('log there')
