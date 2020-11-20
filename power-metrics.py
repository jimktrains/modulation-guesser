#!/usr/bin/env python3

import argparse
from scipy.io import wavfile
from numpy.fft import fft, fftfreq
from numpy.linalg import norm
from numpy import amax, mean, sqrt, square, int32

# Arbitrary constants
bins_for_bandwidth = 5

# Derived constants
bins_to_the_side = int((bins_for_bandwidth - 1)/2) + 1


parser = argparse.ArgumentParser(
    description='Process a signal to give average power in time and freq'
)
parser.add_argument('wavfile', metavar='WAV_FILE', type=str,
                    help='wav file to process')
parser.add_argument('--center_freq', '-c', metavar='CENTER_FREQ', type=int,
                    help='center frequency')
parser.add_argument('--bandwidth', '-b', metavar='BANDWIDTH', type=int,
                    help='bandwidth')

args = parser.parse_args()

samplerate, data = wavfile.read(args.wavfile)

# This is needed because numpy doesn't coearce arrays into larger
# storage types when needed and instead overflows
# ./power-estimator.py:16: RuntimeWarning: invalid value encountered in sqrt
#  print(sqrt(mean(x*conj(x))))
#./power-estimator.py:17: RuntimeWarning: invalid value encountered in sqrt
#  print(sqrt(mean(square(x))))
#./power-estimator.py:18: RuntimeWarning: invalid value encountered in sqrt
#  print(sqrt(mean(square(abs(x)))))
#./power-estimator.py:20: RuntimeWarning: overflow encountered in short_scalars
#  print(sqrt(mean(square([i*i for i in x]))))
#./power-estimator.py:20: RuntimeWarning: invalid value encountered in sqrt
#  print(sqrt(mean(square([i*i for i in x]))))
#
# i=1879, i*i=-8303
data = data.astype(int32)

fft_bin_size = int(args.bandwidth / bins_for_bandwidth)
bincount = int(samplerate / fft_bin_size)
freqs = fftfreq(bincount, 1.0/samplerate)

center_freq_bin = int(args.center_freq / fft_bin_size)

passband_lower_bin = -bins_to_the_side + center_freq_bin
passband_upper_bin = bins_to_the_side + center_freq_bin
passband_range = range(passband_lower_bin, passband_upper_bin + 1)

fft_bins = fft(data, bincount)

# The FFT's results are complex, so normalize them
# and then just filter for the values in our passband.
fft_bins = [norm(fft_bins[b]) for b in passband_range]

# Compute the spectral power and normalized passband
# as our power-over-frequency metric.
normalized_fft_bins = fft_bins / amax(fft_bins)
avg_spec_power = mean(normalized_fft_bins)

# Compute the RMS over time as our power-over-time metric.
rms = sqrt(mean(square(data)))/amax(data)

# Print the report!
print(args.wavfile)
print(f"\trms={rms:5.04}")
print(f"\tavg_spectral_pwr={avg_spec_power:5.04}")
print(f"\tcf±3bins=", end="")

for f in normalized_fft_bins:
    print(f"{f:5.04}", end="\t")
print()
print()
