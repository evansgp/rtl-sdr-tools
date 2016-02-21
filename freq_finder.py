#! /usr/bin/env python3

import argparse
import sys
import rtl_sdr.rtl_power
from statistics import mean, variance

def main():
    parser = rtl_sdr.rtl_power.Parser(args.input_file)
    parser.process()
    spectrum = parser.readings.spectrum
    freqs = analyse(spectrum)
    interesting = sorted(freqs.items(), key=lambda x: x[1], reverse=True)
    print(interesting)

def parse_cli():
    parser = argparse.ArgumentParser(description='Find "active" frequencies in an rtl_power CSV.')
    parser.add_argument('input_file', type=argparse.FileType('r'), nargs='?', default=sys.stdin,
        help='Input CSV file.')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
        help='Verbose output.')
    args = parser.parse_args()
    if args.verbose:
        print('configuration: {!r}'.format(vars(args)))
    return args

def analyse(spectrum):
    # TODO pythonify
    freqs_powers = {}
    freqs = {}
    for (time, bins) in spectrum:
        for (freq, powers) in bins:
            freqs_powers.setdefault(freq, []).append(powers)

    for (freq, powers) in freqs_powers.items():
        f_mean = mean(powers)
        f_var = variance(powers, f_mean)
        f_hits = len([p for p in powers if p > f_mean + 2*f_var])
        if f_hits:
            freqs[freq] = f_hits

    return freqs;


args = parse_cli()
main()
