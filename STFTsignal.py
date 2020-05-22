from scipy.io.wavfile import read
from scipy.signal import stft
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})


def audiosignal(audiofile, info=None, clipLength = 10):
    """
    This function is designed to:
    >>> Shorten an audiofile to amount of samples whithin 10 seconds if length of
        audiofile in seconds is greater than clipLength.
        This is done by evaluating if amount of samples in total is greater than 
        clipLength*samplingrate.
        
        if the audiofile is under clipLength an ValueError is raised

    >>> Only consider the first sound channel if the audio file consist 
        of more than one sound channel.

    Parameters
    ----------
    audiofile : TYPE wav.file
        DESCRIPTION: Chosen audiofile
            
    info : TYPE, optional, bool
        DESCRIPTION: If True, info such as length of audiofile in seconds, in 
                     samples, amount of samples within 10 seconds is calculated 
                     and printed, and number of sound channnels is printed.
                     Default: None
                     
    cliplength : TYPE int
        DESCRIPTION: length of the audio signal in seconds
                     
    Returns
    -------
    samplingrate : samples per second
        
    audio : TYPE, array of int16
            DESCRIPTION: Amplitude content in audiofile

    """
    samplingrate,audio=read(audiofile) #read .wav file
    if info==True: 
        print(f'''
          Input info:
          Length of input signal: {len(audio)/samplingrate:.0f} seconds
          Amount of samples in total: {len(audio):.0f} samples
          Amount of samples within 10 sec: {clipLength*samplingrate} samples
          Number of sound channels: {np.size(audio[0])}
_____________________________________________________________________________
          ''')

    amount_samples_total = len(audio)
    amount_samples = clipLength*samplingrate #Amount of samples in clipLength
    nr_channels = np.size(audio[0]) # amount of channels
    
    if amount_samples_total > amount_samples and nr_channels == 1:
        audio= audio[0:amount_samples]
        print(f'Inputsignal is shortened to samples within {clipLength} s')
    elif amount_samples_total > amount_samples and nr_channels != 1:
        audio= audio[0:amount_samples:, 0] #choose sound channel 1
        print(f'Inputsignal is shortened to samples within {clipLength} s and sound channel 1 is chosen')
    else:
        raise ValueError(f"{audiofile} is under {clipLength} s")
  
    return samplingrate, audio




def stft_of_signal(inputsignal, samplerate, window = 'hanning',windowlength = 2**14,overlap = 0.5, plot=None):
    """
    GENERAL
    ----------
    STFT of inputsignal
    The function uses the function stft from scipy.signal.
    
    
    Parameters
    ----------
    window : TYPE str
        DESCRIPTION: Specifies the applied window function. 
                     If window function is not specified, default: Hanning window
               
    windowlength : TYPE int
        DESCRIPTION: Length of each frame
                     Defaults to: 2**14
            
    overlap : TYPE: float, int
        DESCRIPTION: Percentwise overlap from frame to frame
                     Default: 0.5
            
    inputsignal : TYPE list, tuple, array
        DESCRIPTION: The signal which is analysed
            
    samplerate : TYPE float, int
        DESCRIPTION: samples per second
    
    plot : bool, Optional
        DESCRIPTION: When True, spectrogram of windowed input signal is plotted
                     Default: None

    Returns
    -------
    f : TYPE Array of float 64
        DESCRIPTION: Array of sample frequencies.
            
    t : TYPE Array of float 64
        DESCRIPTION: Array of segment times.
            
    Zxx : TYPE Array of float 64
        DESCRIPTION: STFT of windowed signal          
    """
    f,t,Zxx = stft(inputsignal, fs=samplerate, window=window,
                   nperseg=windowlength, noverlap=int(windowlength*overlap))
    
    
    if plot==True:
        plt.figure()
        plt.pcolormesh(t, f, np.abs(Zxx), vmin=0)
        plt.colorbar()
        plt.title(f'Spectrogram of input signal windowed with {window:} window')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.show()

    Zxx = np.abs(Zxx) 
    Zxx = Zxx[1000:] # Frequencies below are removed
    return f, t, Zxx

def getSTFTofFile(audiofile):
    """
    GENERAL
    ----------
    Computes the Short Time Fourier Transform of the "audiofile".

    Parameters
    ----------
    audiofile : TYPE wav.file
        DESCRIPTION: audiofile path

    Returns
    -------
    Zxx: STFT of file
    """
    samplingrate, audio = audiosignal(audiofile)

    _, _, Zxx = stft_of_signal(audio, samplingrate)
    return Zxx

if __name__ == '__main__':
    #Liste der indeholder lydfilerne
    audiofile =("figur/piano-C4.wav", "figur/trumpet-C4.wav", "lyd/Band of Horses - The Funeral.wav", "lyd/Manowar - Kings of Metal.wav")
    
    Zxx = getSTFTofFile(audiofile[2])
    print(Zxx.shape)
    
    rate, audio = audiosignal(audiofile[2], info=True)

    f, t, Zxx = stft_of_signal(audio,rate,plot=True)