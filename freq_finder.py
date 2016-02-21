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
readings = parser.readings()
print('hz_low ', str(readings.hz_low))
print('hz_high ', str(readings.hz_high))
print('hz_step ', str(readings.hz_step))
print('n_steps  ', str(readings.n_steps))
print(readings.data[0])
print(len(readings.data[0]))
