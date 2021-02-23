import apcmodels.simulation as si
import apcmodels.anf as anf
import numpy as np
from functions import ISOToneGuest2021, GEOMToneGuest2021
import matplotlib.pyplot as plt


def plot_ep(axis_main, F0, condition, level, TMR, title, first, color, fs=int(100e3)):
    """
    Function to plot excitation pattern of a single tone from Experiment 1.

    Arguments:
        axis_main (axis): axis object on which to plot
        F0 (float): F0 of the tone in Hz
        condition (str): condition from which to plot tones, either 'ISO' or 'GEOM'
        title (str): title to add to plot
        first (bool): whether or not this is the first plot in the row
        color ???
    """
    # Set up simulation and stimulus parameters
    params = si.Parameters(F0=F0, F0_masker=F0 * 2 ** (1 / 12), level=level, ten=True, TMR=TMR, fs=fs, cf_low=F0 * 4,
                           cf_high=F0 * 12, n_cf=100, fiber_type='msr')
    params.repeat(10)
    # Synthesize stimuli
    if condition == 'ISO':
        stimulus = ISOToneGuest2021().synthesize_sequence(params)
    else:
        stimulus = GEOMToneGuest2021().synthesize_sequence(params)
    # Add stimulus and flatten
    params.add_inputs(stimulus)
    params.flatten()
    # Estimate responses
    sim = anf.AuditoryNerveZilany2014()
    resp = sim.run(params, parallel=True)
    # Calculate cfs
    cfs = 10**np.linspace(np.log10(F0*4), np.log10(F0*12), 100)
    # Calculate mean over time
    firing_rates = np.array([np.mean(r, axis=1) for r in resp])
    mean_response = np.mean(firing_rates, axis=0)
    sd_response = np.std(firing_rates, axis=0)
    max_response = np.max(mean_response)
    min_response = np.min(mean_response)
    for harmonic in [6, 7, 8, 9, 10]:
        axis_main.plot([harmonic, harmonic], [0, max_response], color='gray', linestyle='dashed', label='_nolegend_')
    axis_main.plot(cfs/F0, mean_response, color=color)
    axis_main.fill_between(cfs/F0, mean_response - sd_response, mean_response + sd_response,
                           color=color, alpha=0.2, label='_nolegend_')
    axis_main.set_xscale('log')
    axis_main.set_ylabel('Firing rate (sp/s)')
    if first:
        axis_main.get_xaxis().set_visible(False)
    if not first:
        axis_main.set_xlabel('CF (Harmonic Number)')
    axis_main.set_ylim((min_response, max_response))
    axis_main.set_title(title)
    axis_main.set_xlim((4, 12))
    axis_main.set_xticks([4, 5, 6, 7, 8, 9, 10, 11, 12])
    axis_main.set_xticklabels([4, 5, 6, 7, 8, 9, 10, 11, 12])

# Plot excitation patterns
f, (a0, a1) = plt.subplots(2, 1, figsize=(3, 4))
plot_ep(a0, 280, 'ISO', 50, 10, '280 Hz', True, '#fc8d62')
plot_ep(a0, 280, 'GEOM', 50, 10, '280 Hz', True, '#8da0cb')
plot_ep(a1, 1400, 'ISO', 50, 10, '1400 Hz', False, '#fc8d62')
plot_ep(a1, 1400, 'GEOM', 50, 10, '1400 Hz', False, '#8da0cb')
plt.legend(['ISO', 'GEOM'])
plt.savefig('plots/fig3.png', bbox_inches='tight')