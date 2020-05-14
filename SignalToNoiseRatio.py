import numpy as np
from STFTsignal import audiosignal, getSTFTofFile, stft_of_signal, FourierAndtimePLOTS
import matplotlib.pyplot as plt
from p2PCA import PCA

audiofile =("lyd/Band of Horses - The Funeral.wav", "lyd/Manowar - Kings of Metal.wav")

def addNoise_and_STFT(audioArray, samplingrate, noice):
    noisyAudio = audioArray + np.random.randn(audioArray.size) * noice
    _, _, ZxxNoisy = stft_of_signal(noisyAudio, samplingrate)
    
    return ZxxNoisy

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

def PCA_and_noise(audiofile, noiceRange="range(0,max(audio)*2, int(max(audio)*2/1000))"):
    ZxxClean = getSTFTofFile(audiofile)
    samplingrate, audio = audiosignal(audiofile)
    
    SNR = [np.var(ZxxClean)/np.var(addNoise_and_STFT(audio, samplingrate, i)) for i in eval(noiceRange)]

    mean, eigenAAT, weighted = PCA(addNoise_and_STFT(audio, samplingrate, 1000))
    
    return mean, eigenAAT, weighted, SNR

# mean, eigenAAT, weighted, SNR = PCA_and_noise(audiofile[1])

# Brug ikke dette(Virker ikke optimalt, LANGSOMT)
# def signal_to_noise_ratio(audio, SNRvalue, tol=0.01):
#     for i in range(0,max(audio)*2, int(max(audio)*2/1000)):
#         if SNRvalue-tol <= np.var(Zxx)/np.var(noisySignal(audio, i)) <= SNRvalue+tol:
#             print(np.var(Zxx)/np.var(noisySignal(audio, i)))
#             print(i)
#             break
#     return i

#a = [signal_to_noise_ratio(audio, i/10, tol=0.01) for i in range (1,11,1)]

#x_axis = [i/10 for i in range(1,11,1)]
#plt.plot(x_axis, a)
