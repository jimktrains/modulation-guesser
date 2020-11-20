# modulation-guesser

This is a little project to attempt to build a metrics
that can guess a digital modulation.

## Hypothesis
Bandwidth, normalized Power Spectrum, and normalized Power-over-Time are
sufficient to guess a modulation or to narrow the options down enough to
manually check with good-enough accuracy.

Initial data: [data.tsv](data.tsv), mirrored on a [https://docs.google.com/spreadsheets/d/1MfwNuRVr6lvTZW3s4uZcxiTbFt6OJsu6mllWj0BigQQ/edit#gid=0](Google Sheet).

## Procedure 

Bandwidth can be a pretty free decision. I plan to round it up to the
nearest 50Hz.

Normalized Power Spectrum is the mean of the 3 bins on each side of and
the center frequency, with each bin being sized to be a fifth of the
bandwidth.

Normalized Power-over-Time is the RMS of the signal normalized by the
largest sample.

The later two are being computed by (power-metrics.py)[power-metrics.py].

Once the computation for each metric has been hammered down, I propose
using the following algorithm to determine the modulation:

1) Filter known modulations by bandwidth
2) Filter modulations for nearness of the known RMS to the Specimen's RMS
3) Rank by RMS of the delta between the Reference Normalized Power
Spectrum  and the Specimen's Normalized Power Spectrum.

