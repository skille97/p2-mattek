from scipy.io.wavfile import read
from scipy.signal import stft
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

rate, audio = read("piano-C4.wav")

def FourierAndtimePLOTS(inputsignal, samplingrate, noise):
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
    inputsignal = inputsignal + np.random.randn(inputsignal.size) * noise
    endpoint_of_fftplot = int(len(inputsignal)/2)
    
    fourier = np.fft.fft(inputsignal)
    fourier = np.abs(fourier)

    freq = np.fft.fftfreq(len(fourier), d=1/samplingrate)
    
    plt.figure()
    plt.plot(freq[0:endpoint_of_fftplot], fourier[0:endpoint_of_fftplot])
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Magnitude")
    plt.savefig(f"C4freq.pdf")

    time = np.linspace(0, len(inputsignal)/samplingrate, len(inputsignal))
    plt.figure()
    plt.plot(time, inputsignal)
    plt.xlabel("Time [s]")
    plt.savefig("C4audio.pdf")


def stftplot(window,windowlength,overlap,inputsignal,samplerate, plot=True):
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
    
    plot :TYPE bool
        DESCRIPTION: When True, a spectrogram of winodwed 
                     inputsignal is plotted. 
                     Default: True

    Returns
    -------
    f : TYPE Array of float 64
        DESCRIPTION: Array of sample frequencies.
            
    t : TYPE Array of float 64
        DESCRIPTION: Array of segment times.
            
    Zxx : TYPE Array of complex64
        DESCRIPTION: STFT of windowed signal          
    """
    
    f,t,Zxx = stft(inputsignal, fs=samplerate, window=window, nfft=windowlength ,nperseg=windowlength, noverlap=windowlength*overlap)     
    
    if plot==True:    
        plt.figure()
        plt.pcolormesh(t, f, np.abs(Zxx), vmin=0,)
        plt.colorbar()
        plt.title(f'STFT Magnitude, window: {window:}')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.savefig(f'spectrogramC4{window}.jpg', dpi=150)
    return f, t, Zxx



if __name__ == '__main__':
    overlap= 0.5
    FourierAndtimePLOTS(audio, rate, 0)
    f,t,Zxx=stftplot('hanning',200,overlap,audio,rate)

