from scipy.io.wavfile import read
from scipy.signal import stft
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})


def audiosignal(audiofile, info=None):
    """
    This function is designed to:
    >>> Shorten an audiofile to amount of samples whithin 10 seconds if length of
        audiofile in seconds is greater than 10 seconds
        This is done by evaluating if amount of samples in total is greater than
    10*samplingrate.
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
                     
    Returns
    -------
    samplingrate : samples per second
        
    audio : TYPE, array of int16
            DESCRIPTION: Amplitude content in audiofile

    """
    samplingrate,audio=read(audiofile)
    
    if info==True:
        print(f'''
          Input info:
          Length of input signal: {len(audio)/samplingrate:.0f} seconds
          Amount of samples in total: {len(audio):.0f} samples
          Amount of samples within 10 sec: {10*samplingrate} samples
          Number of sound channels: {np.size(audio[0])}
_____________________________________________________________________________
          ''')
    
    amount_samples_total = len(audio)
    amount_samples_10s   = 10*samplingrate
    nr_channels = np.size(audio[0])
    
    if amount_samples_total > amount_samples_10s and nr_channels == 1:
        audio= audio[0:10*samplingrate]
        print('Inputsignal is shortened to samples within 10 s')
    elif amount_samples_total > amount_samples_10s and nr_channels != 1:
        audio= audio[0:10*samplingrate:,0]
        print('Inputsignal is shortened to samples within 10 s and sound channel 1 is chosen')
    else:
        audio
  
    return samplingrate, audio

def FourierAndtimePLOTS(inputsignal, samplingrate):
    """
    Plots of inputsignal in time domain and frequency domain.
    Note: The plot of inputsignal in frequency domain is onesided

    Parameters
    ----------
    inputsignal : TYPE array
        DESCRIPTION: the signal to be plotted in time domain and frequency domain
    samplingrate : TYPE int
        DESCRIPTION: The samplingrate of inout signal

    """
    
    endpoint_of_fftplot = int(len(inputsignal)/2)
    
    fourier = np.fft.fft(inputsignal)
    fourier = np.abs(fourier)

    freq = np.fft.fftfreq(len(fourier), d=1/samplingrate)
    
    plt.figure()
    plt.plot(freq[0:endpoint_of_fftplot], fourier[0:endpoint_of_fftplot])
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Magnitude")
    #plt.savefig(f"C4freq.pdf")

    time = np.linspace(0, len(inputsignal)/samplingrate, len(inputsignal))
    plt.figure()
    plt.plot(time, inputsignal, 'r')
    plt.xlabel("Time [s]")
    #plt.savefig("C4audio.pdf")


def stft_of_signal(window,windowlength,overlap,inputsignal,samplerate, plot=None):
    """
    GENERAL
    ----------
    This function takes an input signal and plots a spectrogram of windowed signal.
    The function uses the function stft from scipy.signal.
    
    
    Parameters
    ----------
    window : TYPE str
        DESCRIPTION: Specifies the applied window function. 
                     If window function is not specified, default: Hanning window
               
    windowlength : TYPE int
        DESCRIPTION: Length of each frame
                     Defaults to: 256
            
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
            
    Zxx : TYPE Array of complex64
        DESCRIPTION: STFT of windowed signal          
    """
    f,t,Zxx = stft(inputsignal, fs=samplerate, window=window, nfft=windowlength ,nperseg=windowlength)     
    
    
    if plot==True:
        plt.figure()
        plt.pcolormesh(t, f, np.abs(Zxx), vmin=0)
        plt.colorbar()
        plt.title(f'Spectrogram of input signal windowed with {window:} winow')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
    return f, t, Zxx
      
#Liste der indeholder lydfilerne
audiofile =("piano-C4.wav", "trumpet-C4.wav", "BandofHorses.wav", "KingsOfMetal.wav")

rate, audio = audiosignal(audiofile[0], info=True)

FourierAndtimePLOTS(audio, rate)
f, t, Zxx = stft_of_signal('hanning',2**13,0.5,audio,rate,plot=True)