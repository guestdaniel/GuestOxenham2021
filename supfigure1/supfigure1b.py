"""
This script plots estimates of Q10 for each auditory nerve model (generated by scripts in nofigure/tuning_curves).
Additionally, models of reference data from animals provided by Shera and Guinan (2003) and humans provided by
Oxenham and Shera (2003). Q10 estimates for the Heinz et al. (2001) and Zilany et al. (2014) models are based on
auditory nerve fiber iso-response pure-tone tuning curves. Q10 estimates for the Verhulst et al. (2018) model are
based on QERB estimates derived from basilar membrane impulses responses.

References:
    Oxenham, A. J., & Shera, C. A. (2003). Estimates of human cochlear tuning at low levels using forward and
    simultaneous masking. Journal of the Association for Research in Otolaryngology, 4(4), 541-554.

    Shera, C. A., & Guinan Jr, J. J. (2003). Stimulus-frequency-emission group delay: A test of coherent reflection
    filtering and a window on cochlear tuning. The Journal of the Acoustical Society of America, 113(5), 2762-2772.
"""

import numpy as np
import os, sys
sys.path.append(os.getcwd())
import util as cfg
import matplotlib.pyplot as plt

# Generate and save results
plt.figure(figsize=(4.5, 3.5))
# Load cfs from disk
cfs = np.load(os.path.join('nofigure/tuning_curves/', 'cfs' + '.npy'))
# Loop through models, load that model's q10, and plot
for model_name in ['Heinz2001', 'Zilany2014', 'Verhulst2018']:
    q_10 = np.load(os.path.join('nofigure/tuning_curves/', model_name + '_q10s' + '.npy'))
    plt.plot(cfs/1000, q_10, linewidth=3)
# Handle axes and legend
plt.xscale('log')
plt.yscale('log')
plt.xlabel('CF (kHz)')
plt.ylabel(r'Sharpness ($Q_{10}$)')
plt.legend(['Heinz et al. (2001)', 'Zilany et al. (2014)', 'Verhulst et al. (2018)'])
plt.xlim((0.20, 50))
plt.ylim((1, 20))
# Plot reference data
f_kHz = 10 ** np.linspace(np.log10(200), np.log10(20000), 500) / 1000
def power_law(x, alpha, beta):
    return 1 / 1.82 * beta * x ** alpha  # assume a scaling relationship between q10 and qerb of 1/1.83 (Verschooten et al.)
# Plot cat data
beta = 5.0
alpha = 0.37
plt.plot(f_kHz, power_law(f_kHz, alpha, beta), linestyle='dashed', color='gray', label='_nolegend_')
plt.text(20, 12.5, 'Human', bbox={'edgecolor': 'gray', 'facecolor': 'white'}, color='gray')
# Plot guinea pig data
beta = 4.0
alpha = 0.35
plt.plot(f_kHz, power_law(f_kHz, alpha, beta), linestyle='dashed', color='gray', label='_nolegend_')
plt.text(20, 7.9, 'Cat', bbox={'edgecolor': 'gray', 'facecolor': 'white'}, color='gray')
# Plot guinea pig data
beta = 11.1
alpha = 0.27
plt.plot(f_kHz, power_law(f_kHz, alpha, beta), linestyle='dashed', color='gray', label='_nolegend_')
plt.text(20, 4.4, 'Guinea\nPig', bbox={'edgecolor': 'gray', 'facecolor': 'white'}, color='gray')
# Handle layout
plt.tight_layout()
# Save figure to disk
plt.savefig('plots/supfig1b.png')