"""
The following functions are used throughout the scripts in this repo to synthesize the acoustic stimulus described in
Guest and Oxenham (2021) and to process some of the simulations.
"""
import apcmodels.synthesis as sy
import apcmodels.signal as sg
import numpy as np
from scipy.signal import sosfiltfilt, butter
from scipy.interpolate import interp1d


class ISOToneGuest2021_exp1a(sy.Synthesizer):
    """
    Synthesizes the ISO stimulus in Guest and Oxenham (2021).
    """
    def __init__(self):
        super().__init__(stimulus_name='ISO Tone')

    def synthesize(self, F0, dur=0.350, dur_ramp=0.02, level=None, phase=None, fs=int(48e3), **kwargs):
        """
        Synthesizes a harmonic complex tone composed of components 6-10 of the F0. This is the same stimulus as used
        in Experiment 1a.

        Arguments:
            F0 (float): F0 of the complex tone in Hz
            level (float, ndarray): level per-component of the complex tone in dB SPL, can be either a float (in this
                case, the same level is used for all components) or an ndarray indicating the level of each component
            phase (float, ndarray): phase offset applied to each component of the complex tone in degrees, can be
                either a float (in which case the same phase offset is used for all components) or an ndarray indicating
                the phase offset of each component.
            dur (float): duration in seconds
            dur_ramp (float): duration of raised-cosine ramp in seconds
            fs (int): sampling rate in Hz

        Returns:
            output (array): complex tone stimulus
        """
        # Create array of frequencies, levels, and phases
        freqs = F0*np.array([6, 7, 8, 9, 10])
        if level is None:
            level = 40*np.ones(len(freqs))  # default to 40 dB SPL per component
        elif isinstance(level, float) or isinstance(level, int) is int:
            level = level*np.ones(len(freqs))  # default to 40 dB SPL per component
        if phase is None:
            phase = np.zeros(len(freqs))  # default to sine phase
        elif isinstance(phase, float) or isinstance(phase, int) is int:
            phase = phase + np.zeros(len(freqs))
        # Synthesize, filter, and ramp complex tone signal
        signal = sg.complex_tone(freqs, level, phase, dur, fs)
        signal = sg.cosine_ramp(signal, dur_ramp, fs)
        # Return
        return signal


class ISOToneGuest2021(sy.Synthesizer):
    """
    Synthesizes the ISO stimulus in Guest and Oxenham (2021).
    """
    def __init__(self):
        super().__init__(stimulus_name='ISO Tone')

    def synthesize(self, F0, dur=0.350, dur_ramp=0.02, level=None, phase=None, fs=int(48e3), ten=False, level_noise=0,
                   **kwargs):
        """
        Synthesizes a harmonic complex tone composed of all components of the F0 up to the 24000 Hz (the Nyquist
        frequency for the 48 kHz sampling rate used in the paper). Then, the tone is bandpass filtered from 5.5x to
        10.5x F0 using a zero-phase Butterworth filter. This is the same stimulus as used in Experiment 1b.

        Arguments:
            F0 (float): F0 of the complex tone in Hz
            level (float, ndarray): level per-component of the complex tone in dB SPL, can be either a float (in this
                case, the same level is used for all components) or an ndarray indicating the level of each component
            phase (float, ndarray): phase offset applied to each component of the complex tone in degrees, can be
                either a float (in which case the same phase offset is used for all components) or an ndarray indicating
                the phase offset of each component.
            dur (float): duration in seconds
            dur_ramp (float): duration of raised-cosine ramp in seconds
            ten (bool): whether or not to include threshold-equalizing masking noise
            level_noise (float): the level at which to synthesize the TEN, in dB SPL
            fs (int): sampling rate in Hz

        Returns:
            output (array): complex tone stimulus
        """
        # Set up bandpass filter
        sos = butter(N=6, Wn=[F0 * 5.5 / (fs * 0.5), F0 * 10.5 / (fs * 0.5)], btype="band",
                     output="sos")
        # Create array of frequencies, levels, and phases
        freqs = np.arange(F0, 48000 / 2, F0)  # up to Nyquist for fs=48
        if level is None:
            level = 40*np.ones(len(freqs))  # default to 40 dB SPL per component
        elif type(level) is float or type(level) is int:
            level = level*np.ones(len(freqs))  # default to 40 dB SPL per component
        if phase is None:
            phase = np.zeros(len(freqs))  # default to sine phase
        elif type(phase) is float or type(phase) is int:
            phase = phase + np.zeros(len(freqs))
        # Synthesize, filter, and ramp complex tone signal
        signal = sg.complex_tone(freqs, level, phase, dur, fs)
        signal = sosfiltfilt(sos, signal)
        signal = sg.cosine_ramp(signal, dur_ramp, fs)
        # Synthesize noise
        if ten:
            signal = signal + sg.cosine_ramp(sg.te_noise(dur, fs, 0, fs/2, level_noise), dur_ramp, fs)
        # Return
        return signal


class GEOMToneGuest2021(sy.Synthesizer):
    """
    Synthesizes the GEOM stimulus in Guest and Oxenham (2021).
    """
    def __init__(self):
        super().__init__(stimulus_name='GEOM Tone')

    def synthesize(self, F0, F0_masker, dur=0.350, dur_ramp=0.02, level=None, phase=None, level_masker=None,
                   phase_masker=None, ten=False, level_noise=0, fs=int(48e3), **kwargs):
        """
        Synthesizes a harmonic complex tone composed of all components of the F0 up to the 24000 Hz (the Nyquist
        frequency for the 48 kHz sampling rate used in the paper). Then, the tone is bandpass filtered from 5.5x to
        10.5x F0 using a zero-phase Butterworth filter. This is the same stimulus as used in Experiment 1b.

        Arguments:
            F0 (float): F0 of the complex tone in Hz
            F0_masker (float): F0 of the masker complex tone in Hz
            level (float, ndarray): level per-component of the complex tone in dB SPL, can be either a float (in this
                case, the same level is used for all components) or an ndarray indicating the level of each component.
            phase (float, ndarray): phase offset applied to each component of the complex tone in degrees, can be
                either a float (in which case the same phase offset is used for all components) or an ndarray indicating
                the phase offset of each component.
            dur_ramp (float): duration of raised-cosine ramp in seconds
            ten (bool): whether or not to include threshold-equalizing masking noise
            level_noise (float): the level at which to synthesize the TEN, in dB SPL
            fs (int): sampling rate in Hz

        Returns:
            output (array): complex tone stimulus
        """
        # Set up bandpass filter for the target
        sos = butter(N=6, Wn=[F0 * 5.5 / (fs * 0.5), F0 * 10.5 / (fs * 0.5)], btype="band",
                     output="sos")
        # Set up the bandpass filter for the masker
        sos_masker = butter(N=6, Wn=[F0 * 4 / (fs * 0.5), F0 * 12 / (fs * 0.5)], btype="band",
                     output="sos")
        # Create array of frequencies, levels, and phases
        freqs = np.arange(F0, 48000 / 2, F0)  # up to Nyquist for fs=48
        if level is None:
            level = 40*np.ones(len(freqs))  # default to 40 dB SPL per component
        elif type(level) is float or type(level) is int:
            level = level*np.ones(len(freqs))  # default to 40 dB SPL per component
        if phase is None:
            phase = np.zeros(len(freqs))  # default to sine phase
        elif type(phase) is float or type(phase) is int:
            phase = phase + np.zeros(len(freqs))
        # Synthesize, filter, and ramp complex tone signal
        signal = sg.complex_tone(freqs, level, phase, dur, fs)
        signal = sosfiltfilt(sos, signal)
        signal = sg.cosine_ramp(signal, dur_ramp, fs)
        # Create array of frequencies, levels, and phases for the masker
        freqs_masker = np.arange(F0_masker, 48000 / 2, F0_masker)  # up to Nyquist for fs=48
        if level_masker is None:
            level_masker = 40*np.ones(len(freqs_masker))  # default to 40 dB SPL per component
        elif type(level_masker) is float or type(level_masker) is int:
            level_masker = level_masker*np.ones(len(freqs_masker))  # default to 40 dB SPL per component
        if phase_masker is None:
            phase_masker = np.zeros(len(freqs_masker))  # default to sine phase
        elif type(phase_masker) is float or type(phase_masker) is int:
            phase_masker = phase_masker + np.zeros(len(freqs_masker))
        # Synthesize, filter, and ramp complex tone signal
        masker = sg.complex_tone(freqs_masker, level_masker, phase_masker, dur, fs)
        masker = sosfiltfilt(sos_masker, masker)
        masker = sg.cosine_ramp(masker, dur_ramp, fs)
        # Synthesize noise
        if ten:
            signal = signal + sg.cosine_ramp(sg.te_noise(dur, fs, 0, fs/2, level_noise), dur_ramp, fs)
        # Return
        return signal + masker


class ComplexToneCedolin2005(sy.Synthesizer):
    """
    Synthesizes the complex tone stimulus from Cedolin and Delgutte (2005)
    """
    def __init__(self):
        super().__init__(stimulus_name='Cedolin Tone')

    def synthesize(self, F0=500, level=30, dur=0.2, dur_ramp=0.02, fs=int(48e3), **kwargs):
        """
        Synthesizes the complex tone stimulus from Cedolin and Delgutte (2005)

        Arguments:
            F0 (float): F0 of the complex tone in Hz
            level (float): level per-component of the complex tone in dB SPL
            dur (float): duration in seconds
            dur_ramp (float): duration of raised-cosine ramp in seconds
            fs (int): sampling rate in Hz

        Returns:
            output (array): complex tone stimulus
        """
        # Create array of frequencies, levels, and phases
        freqs = np.arange(start=F0*2, stop=48e3/2, step=F0)
        levels = level*np.ones(len(freqs))
        phases = np.zeros(len(freqs))
        # Synthesize, filter, and ramp complex tone signal
        signal = sg.complex_tone(freqs, levels, phases, dur, fs)
        signal = sg.cosine_ramp(signal, dur_ramp, fs)
        # Return
        return signal


class ComplexToneLarsen2008(sy.Synthesizer):
    """
    Synthesizes the complex tone stimulus from Larsen and Delgutte (2008)
    """
    def __init__(self):
        super().__init__(stimulus_name='Larsen Tone')

    def synthesize(self, F0=500, level=30, dur=0.2, dur_ramp=0.02, fs=int(48e3), ratio=11/9, **kwargs):
        """
        Synthesizes the double complex tone stimulus from Larsen and Delgutte (2008)

        Arguments:
            F0 (float): F0 of the lower complex tone in Hz
            level (float): level per-component of the complex tones in dB SPL
            dur (float): duration in seconds
            dur_ramp (float): duration of raised-cosine ramp in seconds
            fs (int): sampling rate in Hz
            ratio (float): ratio between the F0s of the upper and lower tone

        Returns:
            output (array): complex tone stimulus
        """
        # Create array of frequencies, levels, and phases
        freqs_1 = np.arange(start=F0*2, stop=F0*20, step=F0)
        freqs_2 = np.arange(start=F0*11/9*2, stop=F0*11/9*20, step=F0*11/9)
        levels_1 = level*np.ones(freqs_1.shape)
        levels_2 = level*np.ones(freqs_2.shape)
        phases_1 = np.ones(freqs_1.shape)
        phases_2 = np.ones(freqs_2.shape)
        # Synthesize, filter, and ramp complex tone signals
        x_1 = sg.complex_tone(freqs_1, levels_1, phases_1, dur, fs)
        x_2 = sg.complex_tone(freqs_2, levels_2, phases_2, dur, fs)
        target_1 = sg.cosine_ramp(x_1, dur_ramp, fs) + sg.cosine_ramp(x_2, dur_ramp, fs)
        # Return
        return target_1


def adjust_level(freq, level, model_name):
    """
    Accepts an input level in dB SPL and returns an adjusted level for the corresponding auditory nerve model.
    Adjustments are made based on estimates of absolute threshold for each nerve model made in
    nofigure/absolute_thresholds.

    Parameters:
        freq (float, ndarray): frequency at which the absolute threshold is estimated and used to adjust the level, in
            Hz, or an array of such frequencies
        level (float, ndarray): input level in dB SPL, or an array of such levels
        model_name (str): either 'Heinz2001', 'Zilany2014', or 'Verhulst2018', indicates which model's absolute
            thresholds should be used in the adjustment
    """
    # Branch based on model
    if model_name == 'Heinz2001':
        cfs = np.array([200., 242.30553173, 293.55985352, 355.65588201,
                        430.88693801, 522.03144314, 632.45553203, 766.23736991,
                        928.31776672, 1124.68265038, 1362.58413812, 1650.80837054,
                        2000., 2423.05531726, 2935.59853524, 3556.55882008,
                        4308.86938006, 5220.31443137, 6324.55532034, 7662.37369911,
                        9283.17766723, 11246.82650381, 13625.84138116, 16508.08370536,
                        20000.])
        absolute_thresholds = np.array([11.75338957, 11.62867281, 11.68923837, 11.69510857, 11.71673396,
                                        11.78947423, 11.90428429, 12.0764798, 12.35406782, 12.76388996,
                                        13.21929098, 13.82237866, 14.72409746, 15.62127449, 16.58383025,
                                        17.33935012, 17.71101781, 17.87225817, 17.92201393, 17.9330261,
                                        17.93559906, 17.93581972, 17.93615349, 17.93697896, 17.93698821])
    elif model_name == 'Zilany2014':
        cfs = np.array([200., 242.30553173, 293.55985352, 355.65588201,
                        430.88693801, 522.03144314, 632.45553203, 766.23736991,
                        928.31776672, 1124.68265038, 1362.58413812, 1650.80837054,
                        2000., 2423.05531726, 2935.59853524, 3556.55882008,
                        4308.86938006, 5220.31443137, 6324.55532034, 7662.37369911,
                        9283.17766723, 11246.82650381, 13625.84138116, 16508.08370536,
                        20000.])
        absolute_thresholds = np.array([24.16215997, 21.78254856, 19.98826118, 17.76583852, 15.53689047,
                                        13.21213245, 11.06027241, 9.33326088, 8.29574625, 7.81458668,
                                        7.72554453, 8.32412585, 10.78823985, 10.72308501, 8.244502,
                                        5.5022836, 2.76210577, 0.45029163, -0.36206515, 0.55300722,
                                        4.58129414, 8.37939556, 11.9621168, 15.44527991, 18.74309845])
    elif model_name == 'Verhulst2018':
        cfs = np.array([200., 242.30553173, 293.55985352, 355.65588201,
                        430.88693801, 522.03144314, 632.45553203, 766.23736991,
                        928.31776672, 1124.68265038, 1362.58413812, 1650.80837054,
                        2000., 2423.05531726, 2935.59853524, 3556.55882008,
                        4308.86938006, 5220.31443137, 6324.55532034, 7662.37369911,
                        9283.17766723, 11246.82650381, 13625.84138116, 16508.08370536,
                        20000.])
        absolute_thresholds = np.array([21.87167926, 20.07611191, 19.04426302, 17.29593544, 15.99061908,
                                        15.75462616, 15.60087287, 15.4184775, 16.27429258, 17.40108221,
                                        18.12974557, 20.05392103, 20.87753392, 22.65084918, 23.85382262,
                                        25.55748375, 26.88444276, 28.2902204, 29.30248888, 32.05847776,
                                        33.5721896, 33.88356551, 36.15362977, 40., 40.])
    else:
        raise ValueError('model type is not recognize')
    # Calculate correction and return
    adjustment = interp1d(np.log10(cfs), absolute_thresholds, kind='cubic')
    return level + adjustment(np.log10(freq))
