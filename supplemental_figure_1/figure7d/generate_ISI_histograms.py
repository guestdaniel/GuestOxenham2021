import apcmodels.simulation as si
import apcmodels.anf as anf
import numpy as np
from functions import ComplexToneCedolin2005
import itertools


def calculate_ISI_histograms_Cedolin_2005(F0):
    """
    Synthesizes a complex tone and simulates interspike intervals for an auditory nerve fiber for it. A list of ISIs
    is then saved out to disk.

    Parameters:
        F0 (float): F0 of the complex tone
    """
    # Setup params
    params = si.Parameters(fs=int(200e3), fiber_type='hsr', n_cf=60, cf_low=450, cf_high=9200, F0=F0)
    params.repeat(100)
    params.flatten()

    # Synthesize stimuli and add to params
    stim = ComplexToneCedolin2005()
    params.add_inputs(stim.synthesize_sequence(params))

    # Select model and run
    sim = anf.AuditoryNerveZilany2014()
    results = sim.run(params, runfunc=sim.simulate_spikes)

    # Extract spike times from results
    ISIs = []
    for result in results:
        for idx, channel in result.iterrows():
            spike_times = channel.loc['spikes']
            ISIs.append([np.abs(spike_times[idx[1]] - spike_times[idx[0]]) for idx in
                         itertools.combinations(list(range(len(spike_times))), r=2)])
    ISIs = list(itertools.chain(*ISIs))

    # Return
    return ISIs


# Loop through F0s we want to test, generate ISI histograms, and save to disk
for F0 in [320, 880]:
    ISIs = calculate_ISI_histograms_Cedolin_2005(F0)
    np.save('supplemental_figure_1/figure7d/isi_' + str(F0) + '.npy', ISIs)