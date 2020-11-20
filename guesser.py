#!/usr/bin/env python3

from argparse import ArgumentParser
# Yes, Pandas is overkill for this.
from pandas import read_csv
from numpy import amin, mean, sqrt, square, int32

reference = read_csv('data.tsv', sep='\t')

parser = ArgumentParser(
    description='Guess a modulation based on the given parameters'
)
parser.add_argument('--center_freq', '-c', metavar='CENTER_FREQ', type=int,
                    help='center frequency')
parser.add_argument('--bandwidth', '-b', metavar='BANDWIDTH', type=int,
                    help='bandwidth')
parser.add_argument('--rms', '-r', metavar='RMS', type=float,
                    help='RMS of the signal')
for i in range(-3,4):
    parser.add_argument(f"--spectral-bin-{i:+}", f"-{i+3}", 
                        metavar=f"SPECTRAL_BIN_{i:+}", type=float,
                        help=f"Spectral bin {i:+}",
                        dest=f"spectral_bin_{i+3}")

args = parser.parse_args()

# Filter by the bandwidth
# TODO: perhaps we should normalize the bandwidth inputed
#       and maybe we'd want to grab a bucket above or below as well
#       Since small errors could filter out the canidate?
possible_modulations = reference.loc[reference['Bandwidth (50Hz Bucket)'] == args.bandwidth]

measured_bins = [
        args.spectral_bin_0,
        args.spectral_bin_1,
        args.spectral_bin_2,
        args.spectral_bin_3,
        args.spectral_bin_4,
        args.spectral_bin_5,
        args.spectral_bin_6,
]

# Subtract the reference from the given spectrum and compute the
# RMS of the difference. Lower values mean a better match.
ref_bins = possible_modulations.loc[:,'Freq Bin -3':'Freq Bin +3']
delta_bins = ref_bins - measured_bins
delta_rms = sqrt(mean(square(delta_bins.T)))

# Consider the smallest RMS to be the answer.
best_modulation_idx = delta_rms.idxmin()
print(reference.loc[best_modulation_idx, 'Mode'])
