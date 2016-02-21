#! /usr/bin/env python3

import argparse
import sys
import rtl_sdr.rtl_power

def parse_cli():
    parser = argparse.ArgumentParser(description='Find "active" frequencies in an rtl_power CSV.')
    parser.add_argument('input_file', type=argparse.FileType('r'), nargs='?', default=sys.stdin,
        help='Input CSV file.')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
        help='Verbose output.')
    args = parser.parse_args()
    if args.verbose:
        print(vars(args))
    return args


args = parse_cli()
parser = rtl_sdr.rtl_power.Parser(args.input_file)
parser.process()
readings = parser.readings

first_t = readings.spectrum[0]

print('ts = {}, first = {}, last = {}, bins = {}'.format(first_t[0], first_t[1][0], first_t[1][-1], len(first_t[1])))
#print(first_t)
