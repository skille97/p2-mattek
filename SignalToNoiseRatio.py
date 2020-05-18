import numpy as np
from STFTsignal import audiosignal, getSTFTofFile, stft_of_signal
import matplotlib.pyplot as plt

audiofile =("lyd/Band of Horses - The Funeral.wav", "lyd/Manowar - Kings of Metal.wav")

def addNoise_and_STFT(audioArray, samplingrate, noise):
    """
    Parameters
    ----------
    audioArray : TYPE, array of int16
            DESCRIPTION: Amplitude content in audiofile
    samplingrate : TYPE int
        DESCRIPTION sample rate of audiofile
    noise : TYPE float
        DESCRIPTION variance of added gaussian noise with mean = 0
    Returns
    -------
    ZxxNoisy : TYPE array of float64
        DESCRIPTION STFT of noisy audio
    noisyAudio : TYPE array
        DESCRIPTION Amplitude content in audiofile added noise

    """
    noisyAudio = audioArray + np.random.randn(audioArray.size) * noise #adds noise
    _, _, ZxxNoisy = stft_of_signal(noisyAudio, samplingrate) #STFT
    
    return ZxxNoisy, noisyAudio

def plotSNR(audiofile, noiseRange="range(0,max(audio)*2, int(max(audio)*2/100))"):
    """
    Plot of SNR as a function of variated noise added to audiofile. 
    
    Parameters
    ----------
    audiofile : TYPE .wav file
    noiseRange : TYPE, optional, str
        DESCRIPTION:  range of added noise
        The default is "range(0,max(audio)*2, int(max(audio)*2/100))".

    Returns
    -------
    SNR : TYPE array of SNR values

    """
    ZxxClean = getSTFTofFile(audiofile)
    samplingrate, audio = audiosignal(audiofile)
    
    
    #noise is added in noiseRange
    SNR = [np.var(ZxxClean)/np.var(addNoise_and_STFT(audio, samplingrate, i)[0]) for i in eval(noiseRange)]

    plt.figure()
    plt.grid()
    plt.semilogx(20*np.log(SNR))
    plt.xlabel("samples")
    plt.ylabel("SNR [DB]")
    
    return SNR

if __name__ == '__main__':
    SNR = plotSNR(audiofile[1])
