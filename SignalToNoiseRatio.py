import numpy as np
from STFTsignal import audiosignal, getSTFTofFile, stft_of_signal, FourierAndtimePLOTS
import matplotlib.pyplot as plt

audiofile =("lyd/Band of Horses - The Funeral.wav", "lyd/Manowar - Kings of Metal.wav")


noice=10000

samplingrate, audio = audiosignal(audiofile[1])

noisyAudio = audio + np.random.randn(audio.size) * noice

#FourierAndtimePLOTS(audio, samplingrate)
#FourierAndtimePLOTS(noisyAudio, samplingrate)

_, _, Zxx = stft_of_signal(audio, samplingrate)
_, _, ZxxNoisy = stft_of_signal(noisyAudio, samplingrate)


def noisySignal(audioinput, noice):
    noisyAudio = audioinput + np.random.randn(audioinput.size) * noice
    _, _, ZxxNoisy = stft_of_signal(noisyAudio, samplingrate)
    return ZxxNoisy

SNR = [np.var(Zxx)/np.var(noisySignal(audio, i)) for i in range(0,max(audio)*2, int(max(audio)*2/100))]

plt.figure()
plt.grid()
plt.semilogx(20*np.log(SNR))
plt.xlabel("samples")
plt.ylabel("SNR [DB]")

def signal_to_noise_ratio(audio, SNRvalue, tol=0.01):
    for i in range(0,max(audio)*2, int(max(audio)*2/1000)):
        if SNRvalue-tol <= np.var(Zxx)/np.var(noisySignal(audio, i)) <= SNRvalue+tol:
            print(np.var(Zxx)/np.var(noisySignal(audio, i)))
            print(i)
            break
    return i

#a = [signal_to_noise_ratio(audio, i/10, tol=0.01) for i in range (1,11,1)]

#x_axis = [i/10 for i in range(1,11,1)]
#plt.plot(x_axis, a)
