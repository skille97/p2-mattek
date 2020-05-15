import numpy as np
from STFTsignal import audiosignal, getSTFTofFile, stft_of_signal
import matplotlib.pyplot as plt

audiofile =("lyd/Band of Horses - The Funeral.wav", "lyd/Manowar - Kings of Metal.wav")

def addNoise_and_STFT(audioArray, samplingrate, noice):
    noisyAudio = audioArray + np.random.randn(audioArray.size) * noice
    _, _, ZxxNoisy = stft_of_signal(noisyAudio, samplingrate)
    
    return ZxxNoisy, noisyAudio

def plotSNR(audiofile, noiceRange="range(0,max(audio)*2, int(max(audio)*2/100))"):
    ZxxClean = getSTFTofFile(audiofile)
    samplingrate, audio = audiosignal(audiofile)
    
    SNR = [np.var(ZxxClean)/np.var(addNoise_and_STFT(audio, samplingrate, i)) for i in eval(noiceRange)]

    plt.figure()
    plt.grid()
    plt.semilogx(20*np.log(SNR))
    plt.xlabel("samples")
    plt.ylabel("SNR [DB]")
    
    return SNR

#SNR = plotSNR(audiofile[1])

